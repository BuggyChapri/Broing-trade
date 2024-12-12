const mcc = document.getElementById("marketCapChart");;
const tickers = document.getElementById("priceChangeChart")
const NEWS_API_GLOBAL_DATA = "https://api.coinlore.net/api/global/"
const Cryptocurrency_Tickers = "https://api.coinlore.net/api/tickers/?start=200&limit=100"

function market_data() {
    fetch(NEWS_API_GLOBAL_DATA)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Sorry, unable to fetch data");
            }
            return response.json();
        })
        .then((data) => {
            const globalData = data[0];
            const btc_d = parseFloat(globalData.btc_d)
            const eth_d = parseFloat(globalData.eth_d)
            new Chart(mcc, {
                type: "bar",
                data: {
                    labels: ['BTC Dominance', 'ETH Dominance', 'Others'],
                    datasets: [
                        {
                            data: [btc_d, eth_d, 100 - (btc_d + eth_d)],
                            borderWidth: 1
                        },
                    ],
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch((error) => {
            console.error("Error fetching market data:", error);
        });
}

function Tickers() {
    fetch(Cryptocurrency_Tickers)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Sorry, unable to fetch ticker data");
            }
            return response.json();
        })
        .then((data) => {
            const tk_data = data.data[0];

            let volume24 = parseFloat(tk_data.volume24);
            let market_cap_usd = parseFloat(tk_data.market_cap_usd);
            let percent_change_1h = parseFloat(tk_data.percent_change_1h);
            let percent_change_24h = parseFloat(tk_data.percent_change_24h);
            let percent_change_7d = parseFloat(tk_data.percent_change_7d);
            let csupply = parseFloat(tk_data.csupply);
            let price_usd = parseFloat(tk_data.price_usd);
            let price_btc = parseFloat(tk_data.price_btc);

            new Chart(tickers, {
                type: 'bar',
                data: {
                    labels: ['Market Cap (USD)', '24h Volume (USD)'],
                    datasets: [{
                        label: 'USD Value',
                        data: [market_cap_usd, volume24],
                        backgroundColor: ['#3498db', '#e74c3c'],
                        borderWidth: 1,
                    }],
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'USD',
                            },
                        },
                    },
                    plugins: {
                        legend: {
                            display: true,
                        },
                    },
                },
            });

            const percentChangeChart = document.getElementById("percentChangeChart").getContext("2d");
            new Chart(percentChangeChart, {
                type: 'bar',
                data: {
                    labels: ['1 Hour', '24 Hours', '7 Days'],
                    datasets: [{
                        label: 'Percent Change',
                        data: [percent_change_1h, percent_change_24h, percent_change_7d],
                        borderColor: '#2ecc71',
                        backgroundColor: 'rgba(46, 204, 113, 0.2)',
                        fill: true,
                    }],
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: false,
                            title: {
                                display: true,
                                text: 'Percentage Change',
                            },
                        },
                    },
                    plugins: {
                        legend: {
                            display: true,
                        },
                    },
                },
            });

            const supplyChart = document.getElementById("supplyChart").getContext("2d");
            new Chart(supplyChart, {
                type: 'doughnut',
                data: {
                    labels: ['Circulating Supply (BTC)', 'Price (USD)'],
                    datasets: [{
                        label: 'Bitcoin Metrics',
                        data: [csupply, price_usd],
                        backgroundColor: ['#9b59b6', '#f1c40f'],
                        borderWidth: 1,
                    }],
                },
                options: {
                    plugins: {
                        legend: {
                            display: true,
                        },
                    },
                },
            });
        })
        .catch((error) => {
            console.error("Error fetching ticker data:", error);
        });
}
       
market_data();
Tickers();