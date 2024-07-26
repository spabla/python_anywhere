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
        const progressResponse = await fetch('/getPprogress'); // Your custom route
        if (progressResponse.ok)
        {
            const { progress } = await progressResponse.json();
            progressBar.value = progress;
            if (progress < 100)
            {
                getTimeout(pollProgress, 1000); // Poll every second
            }
            else
            {
                console.error('Error fetching progress');
            }
        }
    }
    catch (error)
    {
        console.error('Network error:', error);
    }
}