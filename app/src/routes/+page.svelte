<script lang="ts">
    let prompt = '';
    let imageUrl: string | null = null;
    let isLoading = false;
    let error: string | null = null;

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
                body: JSON.stringify({ prompt }),
            });
            
            if (!response.ok) {
                throw new Error('Failed to generate image');
            }
            
            const data = await response.json();
            imageUrl = data.url;
        } catch (e) {
            error = e instanceof Error ? e.message : 'An error occurred';
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
    <div class="relative py-3 sm:max-w-xl sm:mx-auto">
        <div class="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
            <div class="max-w-md mx-auto">
                <div class="divide-y divide-gray-200">
                    <div class="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                        <h1 class="text-3xl font-bold text-center mb-8 text-indigo-600">PixelPalette</h1>
                        
                        <form on:submit|preventDefault={generateImage} class="space-y-6">
                            <div>
                                <label for="prompt" class="block text-sm font-medium text-gray-700">
                                    Enter your prompt
                                </label>
                                <div class="mt-1">
                                    <textarea
                                        id="prompt"
                                        bind:value={prompt}
                                        rows="3"
                                        class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                                        placeholder="Describe the image you want to generate..."
                                    ></textarea>
                                </div>
                            </div>

                            <button
                                type="submit"
                                disabled={isLoading}
                                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                            >
                                {isLoading ? 'Generating...' : 'Generate Image'}
                            </button>
                        </form>

                        {#if error}
                            <div class="rounded-md bg-red-50 p-4 mt-4">
                                <div class="text-sm text-red-700">
                                    {error}
                                </div>
                            </div>
                        {/if}

                        {#if imageUrl}
                            <div class="mt-8">
                                <img
                                    src={imageUrl}
                                    alt="Generated artwork"
                                    class="w-full h-auto rounded-lg shadow-lg"
                                />
                                <a
                                    href={imageUrl}
                                    download
                                    class="mt-4 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                                >
                                    Download Image
                                </a>
                            </div>
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
