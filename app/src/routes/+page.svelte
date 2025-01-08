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

<div class="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 p-4">
    <div class="max-w-7xl mx-auto">
        <!-- Desktop: Side by side, Mobile: Stacked -->
        <div class="lg:grid lg:grid-cols-2 lg:gap-6">
            <!-- Controls Column -->
            <div class="bg-white rounded-2xl shadow-xl">
                <!-- Header -->
                <div class="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-5 rounded-t-2xl">
                    <h1 class="text-3xl font-bold text-center text-white">PixelPalette</h1>
                    <p class="text-sm text-center text-indigo-100/90 mt-1">Transform your ideas into stunning AI art</p>
                </div>

                <div class="p-6">
                    <form on:submit|preventDefault={generateImage} class="space-y-6">
                        <!-- Prompt Input -->
                        <div>
                            <label for="prompt" class="block text-base font-medium text-gray-700 mb-2">
                                What would you like to create?
                            </label>
                            <textarea
                                id="prompt"
                                bind:value={prompt}
                                rows="3"
                                class="block w-full px-3.5 py-2.5 text-base border border-gray-200 rounded-xl focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 transition-colors placeholder:text-gray-400"
                                placeholder="Describe your imagination in words..."
                            ></textarea>
                            
                            <!-- Example Prompts -->
                            <div class="mt-2">
                                <div class="flex items-center gap-1.5 text-sm text-gray-500">
                                    <span>Try:</span>
                                    <button
                                        type="button"
                                        class="text-indigo-600 hover:text-indigo-700 hover:underline"
                                        on:click={() => prompt = "A serene Japanese garden with cherry blossoms and a small koi pond"}
                                    >
                                        Japanese Garden
                                    </button>
                                    <span>·</span>
                                    <button
                                        type="button"
                                        class="text-indigo-600 hover:text-indigo-700 hover:underline"
                                        on:click={() => prompt = "A cozy coffee shop at sunset with warm lighting and people reading books"}
                                    >
                                        Cozy Café
                                    </button>
                                    <span>·</span>
                                    <button
                                        type="button"
                                        class="text-indigo-600 hover:text-indigo-700 hover:underline"
                                        on:click={() => prompt = "A futuristic cityscape with flying cars and neon signs"}
                                    >
                                        Future City
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Style and Quality -->
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label for="style" class="block text-sm font-medium text-gray-700 mb-1.5">Art Style</label>
                                <select
                                    id="style"
                                    bind:value={style}
                                    class="block w-full px-3 py-2 text-sm border border-gray-200 rounded-xl focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                                >
                                    {#each styleOptions as option}
                                        <option value={option.value}>{option.label}</option>
                                    {/each}
                                </select>
                            </div>

                            <div>
                                <label for="quality" class="block text-sm font-medium text-gray-700 mb-1.5">Image Quality</label>
                                <select
                                    id="quality"
                                    bind:value={quality}
                                    class="block w-full px-3 py-2 text-sm border border-gray-200 rounded-xl focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                                >
                                    <option value="standard">Standard</option>
                                    <option value="hd">HD Quality</option>
                                </select>
                            </div>
                        </div>

                        <!-- Sliders -->
                        <div class="space-y-5">
                            <div>
                                <div class="flex justify-between items-center mb-2">
                                    <label class="text-sm font-medium text-gray-700">Creativity</label>
                                    <span class="text-sm text-indigo-600">{creativity}%</span>
                                </div>
                                <input 
                                    type="range" 
                                    bind:value={creativity} 
                                    min="0" 
                                    max="100"
                                    class="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                                />
                            </div>

                            <div>
                                <div class="flex justify-between items-center mb-2">
                                    <label class="text-sm font-medium text-gray-700">Detail Level</label>
                                    <span class="text-sm text-indigo-600">{detailLevel}%</span>
                                </div>
                                <input 
                                    type="range" 
                                    bind:value={detailLevel} 
                                    min="0" 
                                    max="100"
                                    class="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                                />
                            </div>

                            <div>
                                <div class="flex justify-between items-center mb-2">
                                    <label class="text-sm font-medium text-gray-700">Mood Intensity</label>
                                    <span class="text-sm text-indigo-600">{moodIntensity}%</span>
                                </div>
                                <input 
                                    type="range" 
                                    bind:value={moodIntensity} 
                                    min="0" 
                                    max="100"
                                    class="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                                />
                            </div>
                        </div>

                        <!-- Generate Button -->
                        <button
                            type="submit"
                            disabled={isLoading}
                            class="w-full py-3 text-sm font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
                        >
                            {#if isLoading}
                                <div class="flex items-center justify-center gap-2">
                                    <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    <span>Creating...</span>
                                </div>
                            {:else}
                                Generate Image
                            {/if}
                        </button>

                        <!-- Error Message -->
                        {#if error}
                            <div class="rounded-xl bg-red-50 p-3 border border-red-100">
                                <div class="flex gap-2">
                                    <svg class="h-4 w-4 text-red-400 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                                    </svg>
                                    <p class="text-sm text-red-700">{error}</p>
                                </div>
                            </div>
                        {/if}
                    </form>
                </div>
            </div>

            <!-- Image Preview Column -->
            <div class="mt-6 lg:mt-0">
                <div class="bg-white rounded-2xl shadow-xl flex flex-col h-full">
                    <div class="flex-1 flex flex-col">
                        {#if imageUrl}
                            <div class="relative flex-1 min-h-0 flex flex-col">
                                <div class="relative flex-1">
                                    <img
                                        id="generated-image"
                                        src={imageUrl}
                                        alt="Generated artwork"
                                        class="absolute inset-0 w-full h-full object-cover rounded-t-2xl"
                                    />
                                    {#if isLoading}
                                        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center rounded-t-2xl">
                                            <div class="flex flex-col items-center gap-2">
                                                <svg class="animate-spin h-8 w-8 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                                </svg>
                                                <p class="text-sm text-white font-medium">Creating...</p>
                                            </div>
                                        </div>
                                    {/if}
                                </div>
                                <div class="p-4 bg-white rounded-b-2xl border-t border-gray-100">
                                    <div class="flex items-center justify-between">
                                        <div class="flex items-center gap-2">
                                            <svg class="w-5 h-5 text-indigo-500" viewBox="0 0 20 20" fill="currentColor">
                                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                                            </svg>
                                            <span class="text-sm text-gray-600">Image generated successfully</span>
                                        </div>
                                        <button
                                            on:click={() => imageUrl && window.open(imageUrl, '_blank')}
                                            class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-colors duration-200 shadow-sm"
                                        >
                                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                                            </svg>
                                            Download
                                        </button>
                                    </div>
                                </div>
                            </div>
                        {:else if isLoading}
                            <div class="flex-1 flex items-center justify-center p-6 bg-gradient-to-b from-white to-gray-50 rounded-2xl">
                                <div class="flex flex-col items-center gap-2">
                                    <svg class="animate-spin h-8 w-8 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    <p class="text-sm text-gray-500">Creating your masterpiece...</p>
                                </div>
                            </div>
                        {:else}
                            <div class="flex-1 flex flex-col items-center justify-center p-6 text-center border-2 border-dashed border-gray-200 m-6 rounded-xl bg-gradient-to-b from-white to-gray-50">
                                <div class="bg-indigo-50 p-4 rounded-full mb-4">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                <h3 class="text-xl font-semibold text-gray-900 mb-2">Create Your Masterpiece</h3>
                                <p class="text-gray-500 mb-6">Enter your prompt on the left and watch as AI transforms your words into stunning artwork.</p>
                                <div class="space-y-3 text-sm text-gray-600">
                                    <div class="flex items-center gap-2">
                                        <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                        </svg>
                                        <span>Choose from 8 unique art styles</span>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                        </svg>
                                        <span>Fine-tune with interactive sliders</span>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                        </svg>
                                        <span>Generate in HD quality</span>
                                    </div>
                                </div>
                            </div>
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
