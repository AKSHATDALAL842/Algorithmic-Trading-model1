
document.addEventListener('DOMContentLoaded', () => {
    const runBacktestBtn = document.getElementById('run-backtest-btn');
    const metricsDiv = document.getElementById('metrics');
    const tradesTableBody = document.querySelector('#trades-table tbody');
    const equityChartCanvas = document.getElementById('equity-chart');
    let equityChart;

    runBacktestBtn.addEventListener('click', async () => {
        console.log("Running backtest...");
        await fetch('/api/run_backtest', { method: 'POST' });
        console.log("Backtest complete. Fetching results...");
        const response = await fetch('/api/get_results');
        const data = await response.json();
        updateDashboard(data);
    });

    function updateDashboard(data) {
        // Update metrics
        metricsDiv.innerHTML = `
            <p><strong>Final Cash:</strong> $${data.final_cash.toFixed(2)}</p>
            <p><strong>Total Trades:</strong> ${data.total_trades}</p>
            <p><strong>Net P&L:</strong> $${data.pnl.toFixed(2)}</p>
        `;

        // Update trades table
        tradesTableBody.innerHTML = '';
        data.trades.forEach(trade => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${trade.timestamp}</td>
                <td>${trade.symbol}</td>
                <td>${trade.side}</td>
                <td>${trade.price.toFixed(2)}</td>
                <td>${trade.quantity}</td>
            `;
            tradesTableBody.appendChild(row);
        });

        // Update equity chart
        if (equityChart) {
            equityChart.destroy();
        }
        equityChart = new Chart(equityChartCanvas, {
            type: 'line',
            data: {
                labels: data.equity_curve.timestamps,
                datasets: [{
                    label: 'Equity',
                    data: data.equity_curve.equity,
                    borderColor: '#007bff',
                    tension: 0.1
                }]
            },
            options: {
                scales: {
                    x: {
                        ticks: {
                            maxTicksLimit: 20
                        }
                    }
                }
            }
        });
    }
});
