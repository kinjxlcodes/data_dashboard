document.addEventListener('DOMContentLoaded', function () {
    const yearFilter = document.getElementById('year-filter');
    const countryFilter = document.getElementById('country-filter');
    const topicFilter = document.getElementById('topic-filter');
    const regionFilter = document.getElementById('region-filter');
    const applyFiltersButton = document.getElementById('apply-filters');
    const chart = document.getElementById('chart');

    function populateFilters(data) {
        const years = [...new Set(data.map(d => d.year))];
        const countries = [...new Set(data.map(d => d.country))];
        const topics = [...new Set(data.map(d => d.topic))];
        const regions = [...new Set(data.map(d => d.region))];

        years.forEach(year => {
            const option = document.createElement('option');
            option.value = year;
            option.text = year;
            yearFilter.appendChild(option);
        });

        countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country;
            option.text = country;
            countryFilter.appendChild(option);
        });

        topics.forEach(topic => {
            const option = document.createElement('option');
            option.value = topic;
            option.text = topic;
            topicFilter.appendChild(option);
        });

        regions.forEach(region => {
            const option = document.createElement('option');
            option.value = region;
            option.text = region;
            regionFilter.appendChild(option);
        });
    }

    function fetchData() {
        let query = '/api/data?';
        const filters = {
            year: yearFilter.value,
            country: countryFilter.value,
            topic: topicFilter.value,
            region: regionFilter.value
        };

        for (let key in filters) {
            if (filters[key]) {
                query += `${key}=${filters[key]}&`;
            }
        }

        fetch(query)
            .then(response => response.json())
            .then(data => drawChart(data));
    }

    function drawChart(data) {
        const xValues = data.map(d => d.country);
        const yValues = data.map(d => d.intensity);

        const trace = {
            x: xValues,
            y: yValues,
            type: 'bar'
        };

        const layout = {
            title: 'Intensity by Country',
            xaxis: {
                title: 'Country'
            },
            yaxis: {
                title: 'Intensity'
            }
        };

        Plotly.newPlot(chart, [trace], layout);
    }

    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            populateFilters(data);
            drawChart(data);
        });

    applyFiltersButton.addEventListener('click', fetchData);
});
