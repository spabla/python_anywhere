const updateLocalDatabaseButton = document.getElementById('updateLocalDatabase')
updateLocalDatabaseButton.addEventListener('click', async () => {
    try
    {
        const response = await fetch('/updateLocalDatabase', { method: 'POST' });
        if (response.ok)
        {
            // Process started successfully
            // Poll the backend for progress updates
            pollProgress();

            updateLocalDatabaseButton.disabled = true; // Disable the button
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
            const progressBar = document.getElementById('progressBar')
            progressBar.value = progress;
            if (progress < 100)
            {
                setTimeout(pollProgress, 1000); // Poll every second
            }
            else
            {
                const updateLocalDatabaseButton = document.getElementById('updateLocalDatabase')
                updateLocalDatabaseButton.disabled = false; // enable the button
            }
        }
    }
    catch (error)
    {
        console.error('Network error:', error);
    }
}