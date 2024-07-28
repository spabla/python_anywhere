const updateLocalDatabaseButton = document.getElementById('updateLocalDatabase');
const progressBar = document.getElementById('progressBar');

updateLocalDatabaseButton.addEventListener('click', async () => {
    try
    {
        const response = await fetch('/updateLocalDatabase', { method: 'POST' });
        if (response.ok)
        {
            // Process started successfully
            // Poll the backend for progress updates
            pollProgress();
        }
        else
        {
            console.error('Error starting process');
        }
    }
    catch (error)
    {
        onsole.error('Network error:', error);
    }
});

async function pollProgress()
{
    try
    {
        const progressResponse = await fetch('/getProgress', { method: 'POST' }); // Your custom route
        if (progressResponse.ok)
        {
            const { progress } = await progressResponse.json();
            progressBar.value = progress;
            if (progress < 100)
            {
                setTimeout(pollProgress, 1000); // Poll every second
            }
        }
    }
    catch (error)
    {
        console.error('Network error:', error);
    }
}