document.addEventListener('DOMContentLoaded', () => {

    const searchBar = document.getElementById('search-bar');
    const loadingDiv = document.getElementById('loading');
    const noMatchDiv = document.getElementById('no-matches');
    const resultsDiv = document.getElementById('results');

    // Get intitial results from URL
    fetchResults();

    // Debounced searches when user types
    let debounceTimer;
    searchBar.addEventListener('input', () => {
        showLoading();
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(fetchResults, 300); // 300ms delay
    });

    function fetchResults() {
        var query = searchBar.value.trim();
        if (query === '') {
            showNoMatch();
            return;
        }
        console.log(`Getting results for '${query}'...`);
        fetch(`/api/tmdb/search/movie?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (!data || data.length === 0 || data.total_results === 0) {
                showNoMatch();
                return;
            }
            renderResults(data);
        })
        .catch(error => console.log(error));
    }

    function renderResults(data) {
        resultsDiv.innerHTML = ''; // Clear old results
        data.results.forEach(item => {

            // Define structure of result card
            const result = document.createElement('div');
            const row = document.createElement('div');
            const col1 = document.createElement('div');
            const col2 = document.createElement('div');
            const body = document.createElement('div');

            result.classList.add('card', 'border-top-0', 'border-start-0', 'border-end-0', 'mb-2');
            row.classList.add('row');
            col1.classList.add('col-4', 'col-md-2', 'mb-2');
            col2.classList.add('col-8');
            body.classList.add('card-body');
            
            // Add poster to the card
            const poster = document.createElement('img');
            if (item.poster_path) {
                poster.src = `${tmdbImages}w92${item.poster_path}`;
            }
            else {
                poster.src = `${staticImages}no_poster_92.jpg`;
            }
            poster.classList.add('img-fluid', 'rounded');
            poster.alt = item.title;
            
            // Add title and link it to item page
            const title = document.createElement('h5');
            title.classList.add('card-title');
            title.innerHTML = `<a href="/movie/${item.id}" class="stretched-link link-body-emphasis link-offset-1 link-underline-opacity-0 link-underline-opacity-25-hover">${item.title}</a>
            <small class="text-body-secondary">(${item.release_date.slice(0, 4)})</small>`;
            
            // Add info to the card
            const overview = document.createElement('p');
            overview.classList.add('card-text');
            if (item.overview.length >= 200) {
                overview.innerHTML = item.overview.slice(0, 197) + '...';
            }
            else {
                overview.innerHTML = item.overview;
            }
            
            // Construct and add the result card
            col1.append(poster);
            body.append(title, overview);
            col2.append(body);
            row.append(col1, col2);
            result.append(row);
            resultsDiv.appendChild(result);
        });
        showResults();
    }

    function showLoading() {
        noMatchDiv.style.display = 'none';
        resultsDiv.style.display = 'none';
        loadingDiv.style.display = 'block';
    }

    function showNoMatch() {
        loadingDiv.style.display = 'none';
        resultsDiv.style.display = 'none';
        noMatchDiv.style.display = 'block';
    }

    function showResults() {
        noMatchDiv.style.display = 'none';
        loadingDiv.style.display = 'none';
        resultsDiv.style.display = 'block';
    }
});