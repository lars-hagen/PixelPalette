<script lang="ts">
    let prompt = '';
    let imageUrl: string | null = null;
    let isLoading = false;
    let error: string | null = null;
    let quality: 'standard' | 'hd' = 'standard';
    let style: string = 'natural';
    let creativity: number = 50;
    let detailLevel: number = 50;
    let moodIntensity: number = 50;

    const styleOptions = [
        { value: 'natural', label: 'Natural Photography' },
        { value: 'vivid', label: 'Vivid Colors' },
        { value: 'anime', label: 'Anime Style' },
        { value: 'fantasy', label: 'Fantasy Art' },
        { value: 'cyberpunk', label: 'Cyberpunk' },
        { value: 'minimalist', label: 'Minimalist' },
        { value: 'watercolor', label: 'Watercolor Painting' },
        { value: 'retro', label: 'Retro/Vintage' }
    ];

    function getEnhancedPrompt(basePrompt: string): string {
        const creativityAdjective = creativity > 75 ? 'highly imaginative and unique' 
            : creativity > 50 ? 'creative' 
            : 'straightforward';
        
        const detailAdjective = detailLevel > 75 ? 'highly detailed and intricate' 
            : detailLevel > 50 ? 'detailed' 
            : 'simple';
            
        const moodAdjective = moodIntensity > 75 ? 'dramatic and intense' 
            : moodIntensity > 50 ? 'expressive' 
            : 'subtle';

        return `Create a ${creativityAdjective}, ${detailAdjective}, ${moodAdjective} ${basePrompt}`;
    }

    function scrollToImage() {
        if (window.innerWidth < 1024) {  // mobile only
            setTimeout(() => {
                document.getElementById('generated-image')?.scrollIntoView({ behavior: 'smooth' });
            }, 100);
        }
    }

    async function generateImage() {
        if (!prompt.trim()) return;
        
        isLoading = true;
        error = null;
        
        try {
            const response = await fetch('http://127.0.0.1:5000/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    prompt: getEnhancedPrompt(prompt),
                    quality,
                    style,
                    creativity,
                    detailLevel,
                    moodIntensity
                }),
            });
            
            if (!response.ok) {
                throw new Error('Failed to generate image');
            }
            
            const data = await response.json();
            imageUrl = data.url;
            scrollToImage();
        } catch (e) {
            error = e instanceof Error ? e.message : 'An error occurred';
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 py-6 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
        <div class="lg:grid lg:grid-cols-2 lg:gap-8">
            <!-- Controls Column -->
            <div class="bg-white rounded-2xl shadow-xl overflow-hidden mb-8 lg:mb-0">
                <!-- Header -->
                <div class="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-4">
                    <h1 class="text-3xl font-bold text-center text-white">PixelPalette</h1>
                    <p class="text-center text-indigo-100 mt-1">Transform your ideas into stunning AI art</p>
                </div>

                <!-- Main Content -->
                <div class="p-6 sm:p-8">
                    <form on:submit|preventDefault={generateImage} class="space-y-8">
                        <!-- Prompt Input -->
                        <div class="space-y-2">
                            <label for="prompt" class="block text-sm font-medium text-gray-700">
                                What would you like to create?
                            </label>
                            <div class="relative">
                                <textarea
                                    id="prompt"
                                    bind:value={prompt}
                                    rows="3"
                                    class="block w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-sm placeholder:text-gray-400"
                                    placeholder="Describe your imagination in words..."
                                ></textarea>
                            </div>
                        </div>

                        <!-- Style Selection -->
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div class="space-y-2">
                                <label for="style" class="block text-sm font-medium text-gray-700">
                                    Art Style
                                </label>
                                <select
                                    id="style"
                                    bind:value={style}
                                    class="block w-full px-4 py-2.5 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-sm"
                                >
                                    {#each styleOptions as option}
                                        <option value={option.value}>{option.label}</option>
                                    {/each}
                                </select>
                            </div>

                            <div class="space-y-2">
                                <label for="quality" class="block text-sm font-medium text-gray-700">
                                    Image Quality
                                </label>
                                <select
                                    id="quality"
                                    bind:value={quality}
                                    class="block w-full px-4 py-2.5 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all text-sm"
                                >
                                    <option value="standard">Standard</option>
                                    <option value="hd">HD Quality</option>
                                </select>
                            </div>
                        </div>

                        <!-- Sliders -->
                        <div class="space-y-6">
                            <div class="space-y-2">
                                <div class="flex justify-between items-center">
                                    <label class="block text-sm font-medium text-gray-700">
                                        Creativity Level
                                    </label>
                                    <span class="text-xs text-indigo-600 font-medium">
                                        {creativity}%
                                    </span>
                                </div>
                                <div class="flex items-center gap-3">
                                    <span class="text-xs text-gray-500">Conservative</span>
                                    <input 
                                        type="range" 
                                        bind:value={creativity} 
                                        min="0" 
                                        max="100"
                                        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                                    />
                                    <span class="text-xs text-gray-500">Experimental</span>
                                </div>
                            </div>

                            <div class="space-y-2">
                                <div class="flex justify-between items-center">
                                    <label class="block text-sm font-medium text-gray-700">
                                        Detail Level
                                    </label>
                                    <span class="text-xs text-indigo-600 font-medium">
                                        {detailLevel}%
                                    </span>
                                </div>
                                <div class="flex items-center gap-3">
                                    <span class="text-xs text-gray-500">Simple</span>
                                    <input 
                                        type="range" 
                                        bind:value={detailLevel} 
                                        min="0" 
                                        max="100"
                                        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                                    />
                                    <span class="text-xs text-gray-500">Complex</span>
                                </div>
                            </div>

                            <div class="space-y-2">
                                <div class="flex justify-between items-center">
                                    <label class="block text-sm font-medium text-gray-700">
                                        Mood Intensity
                                    </label>
                                    <span class="text-xs text-indigo-600 font-medium">
                                        {moodIntensity}%
                                    </span>
                                </div>
                                <div class="flex items-center gap-3">
                                    <span class="text-xs text-gray-500">Subtle</span>
                                    <input 
                                        type="range" 
                                        bind:value={moodIntensity} 
                                        min="0" 
                                        max="100"
                                        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                                    />
                                    <span class="text-xs text-gray-500">Dramatic</span>
                                </div>
                            </div>
                        </div>

                        <!-- Generate Button -->
                        <button
                            type="submit"
                            disabled={isLoading}
                            class="w-full py-3 px-4 border border-transparent rounded-xl shadow-sm text-sm font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 transition-all duration-200 transform hover:scale-[1.02]"
                        >
                            {#if isLoading}
                                <div class="flex items-center justify-center gap-2">
                                    <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    <span>Generating...</span>
                                </div>
                            {:else}
                                Generate Image
                            {/if}
                        </button>
                    </form>

                    <!-- Error Message -->
                    {#if error}
                        <div class="mt-6 rounded-xl bg-red-50 p-4 border border-red-100">
                            <div class="flex">
                                <div class="flex-shrink-0">
                                    <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                                    </svg>
                                </div>
                                <div class="ml-3">
                                    <p class="text-sm text-red-700">{error}</p>
                                </div>
                            </div>
                        </div>
                    {/if}
                </div>
            </div>

            <!-- Image Column -->
            {#if imageUrl || isLoading}
                <div class="lg:sticky lg:top-8" id="generated-image">
                    <div class="bg-white rounded-2xl shadow-xl overflow-hidden p-6">
                        <div class="relative">
                            {#if imageUrl}
                                <div class="space-y-4">
                                    <div class="relative rounded-xl overflow-hidden shadow-lg">
                                        <img
                                            src={imageUrl}
                                            alt="Generated artwork"
                                            class="w-full h-auto"
                                        />
                                        {#if isLoading}
                                            <div class="absolute inset-0 bg-black/50 backdrop-blur-sm rounded-xl flex items-center justify-center">
                                                <div class="flex flex-col items-center gap-4">
                                                    <svg class="animate-spin h-8 w-8 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                                    </svg>
                                                    <p class="text-sm text-white font-medium">Creating your masterpiece...</p>
                                                </div>
                                            </div>
                                        {:else}
                                            <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
                                        {/if}
                                    </div>
                                    <a
                                        href={imageUrl}
                                        download
                                        class="block w-full text-center py-3 px-4 rounded-xl text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors duration-200"
                                    >
                                        Download Image
                                    </a>
                                </div>
                            {:else}
                                <div class="h-[512px] flex items-center justify-center bg-gray-50 rounded-xl">
                                    <div class="flex flex-col items-center gap-4">
                                        <svg class="animate-spin h-8 w-8 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                        <p class="text-sm text-gray-500">Creating your masterpiece...</p>
                                    </div>
                                </div>
                            {/if}
                        </div>
                    </div>
                </div>
            {:else}
                <div class="lg:sticky lg:top-8">
                    <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
                        <div class="bg-gradient-to-r from-indigo-100 to-purple-100 px-6 py-4">
                            <h2 class="text-xl font-semibold text-indigo-900">Welcome to PixelPalette!</h2>
                        </div>
                        <div class="p-6">
                            <div class="space-y-6">
                                <div class="text-gray-600">
                                    <h3 class="font-medium mb-2">Try these example prompts:</h3>
                                    <ul class="space-y-2 text-sm">
                                        <li class="p-2 bg-indigo-50 rounded-lg hover:bg-indigo-100 cursor-pointer transition-colors" 
                                            on:click={() => prompt = "A serene Japanese garden with cherry blossoms and a small koi pond"}>
                                            "A serene Japanese garden with cherry blossoms and a small koi pond"
                                        </li>
                                        <li class="p-2 bg-indigo-50 rounded-lg hover:bg-indigo-100 cursor-pointer transition-colors"
                                            on:click={() => prompt = "A cozy coffee shop at sunset with warm lighting and people reading books"}>
                                            "A cozy coffee shop at sunset with warm lighting and people reading books"
                                        </li>
                                        <li class="p-2 bg-indigo-50 rounded-lg hover:bg-indigo-100 cursor-pointer transition-colors"
                                            on:click={() => prompt = "A futuristic cityscape with flying cars and neon signs"}>
                                            "A futuristic cityscape with flying cars and neon signs"
                                        </li>
                                    </ul>
                                </div>

                                <div class="border-t border-gray-200 pt-6">
                                    <h3 class="font-medium mb-3 text-gray-700">Pro Tips:</h3>
                                    <ul class="space-y-3 text-sm text-gray-600">
                                        <li class="flex gap-2 items-start">
                                            <svg class="h-5 w-5 text-indigo-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                                            </svg>
                                            <span>Be specific with details like colors, lighting, and mood</span>
                                        </li>
                                        <li class="flex gap-2 items-start">
                                            <svg class="h-5 w-5 text-indigo-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                                            </svg>
                                            <span>Try different art styles to find the perfect look</span>
                                        </li>
                                        <li class="flex gap-2 items-start">
                                            <svg class="h-5 w-5 text-indigo-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                                            </svg>
                                            <span>Adjust the sliders to fine-tune the generation</span>
                                        </li>
                                    </ul>
                                </div>

                                <div class="bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl p-4 text-white">
                                    <p class="text-sm">
                                        Ready to create? Start by typing your prompt above and adjust the settings to your liking!
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            {/if}
        </div>
    </div>
</div>
