const dropdown = document.getElementById('driver1_dropdown');
dropdown.addEventListener('change', async () => {
    const selectedItem = dropdown.value;
    try {
        const response = await fetch('/process_item', {
            method: 'POST',
            body: new URLSearchParams({ selected_item: selectedItem }),
        });
        const data = await response.json();
        console.log(data.message);
    } catch (error) {
        console.error('Error sending data to backend:', error);
        }
});

const dropdown2 = document.getElementById('driver2_dropdown');
dropdown2.addEventListener('change', async () => {
    const selectedItem = dropdown2.value;
    try {
        const response = await fetch('/process_item', {
            method: 'POST',
            body: new URLSearchParams({ selected_item: selectedItem }),
        });
        const data = await response.json();
        console.log(data.message);
    } catch (error) {
        console.error('Error sending data to backend:', error);
        }
});

async function goSimulatedRacing()
{
    const driver1Combo = document.getElementById("driver1_dropdown");
    const driver2Combo = document.getElementById("driver2_dropdown");
    console.log(driver1Combo.value);
    console.log(driver2Combo.value);
    driver1Value = driver1Combo.value;
    driver2Value = driver2Combo.value;
    try
    {
        const response = await fetch('/runSimulatedRaces', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "driver1": driver1Value,
                "driver2": driver2Value,
            }),
        });

        const data = await response.json();
        console.log(data);

        // Populate the table rows dynamically
        let driver1WinCount = 0;
        let driver2WinCount = 0;
        table = document.getElementById('RaceResultTable');
        if (table !== null)
        {
            table.remove();
        }
        table= document.createElement('table')
        table.id = "RaceResultTable"
        const tableHead = document.createElement('tHead')
        table.appendChild(tableHead);
        const tableBody = document.createElement('tBody');
        table.appendChild(tableBody);
        const row = document.createElement('tr');
        row.innerHTML = `
            <th style="border: 1px solid black;">Grand Prix</th>
            <th style="border: 1px solid black;">Circuit</th>
            <th style="border: 1px solid black;">Driver 1 Time</th>
            <th style="border: 1px solid black;">Driver 2 Time</th>
            <th style="border: 1px solid black;">Winner</th>`;
        tableHead.appendChild(row);

        data.forEach(entry => {
            let circuit = entry['circuit'];
            let driver1BestYear = entry['Driver 1 Best Year'];
            let driver1BestTime = entry['Driver 1 Best Time'];
            let driver1BestTimeAfterComp = entry['Driver 1 Best Time after Comp'];
            let driver2BestYear = entry['Driver 2 Best Year'];
            let driver2BestTime = entry['Driver 2 Best Time'];
            let driver2BestTimeAfterComp = entry['Driver 2 Best Time after Comp'];
            let raceWinner = entry['Race Winner after Comp'];

            if (raceWinner === driver1Value)
            {
                driver1WinCount++;
            }
            else
            {
                driver2WinCount++;
            }

            const row = document.createElement('tr');
            const driver1TimeFormatted = new Date(driver1BestTimeAfterComp).toISOString().substr(11, 8)
            const driver2TimeFormatted = new Date(driver2BestTimeAfterComp).toISOString().substr(11, 8)
            row.innerHTML = `
                <td style="border: 1px solid black;">"Unknown"</td>
                <td style="border: 1px solid black;">${circuit}</td>
                <td style="border: 1px solid black;">
                    <a href="driver_time_rationale.html?driver1Value=${driver1Value}
                        &circuit=${circuit}
                        &driver1BestYear=${driver1BestYear}
                        &driver1BestTime=${driver1BestTime}
                        &driver1BestTimeAfterComp=${driver1BestTimeAfterComp}"> ${driver1TimeFormatted}</a>
                </td>
                <td style="border: 1px solid black;">
                    <a href="driver_time_rationale.html?driver2Value=${driver2Value} \
                        &circuit=${circuit} \
                        &driver2BestYear=${driver2BestYear} \
                        &driver2BestTime=${driver2BestTime} \
                        &driver2BestTimeAfterComp=${driver2BestTimeAfterComp}">
                        ${driver2TimeFormatted}</a>
                </td>
                <td style="border: 1px solid black;">${raceWinner}</td>
            `;
            tableBody.appendChild(row);
        });

        document.body.appendChild(table)

        winnerMessage = document.getElementById('the-winner-message');
        if (winnerMessage !== null)
        {
            winnerMessage.remove();
        }
        winnerMessage = document.createElement('h2');
        winnerMessage.id = "the-winner-message"
        winnerMessage.style.color = 'red';
        if (driver1WinCount > driver2WinCount)
        {
            winnerMessage.textContent = `Champion of Champions is: ${driver1Value}`;
        }
        else
        {
            if (driver2WinCount > driver1WinCount)
            {
                winnerMessage.textContent = `Champion of Champions is: ${driver2Value}`;
            }
            else
            {
                winnerMessage.textContent ='We have a draw';
            }
        }
        document.body.appendChild(winnerMessage);
    }
    catch (error)
    {
        console.error('Error sending data to backend:', error);
    }
}
