document.addEventListener('DOMContentLoaded', () => {

    const movieCountDiv = document.getElementById('movie-count');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const moviesDiv = document.getElementById('movies');
    const sortMenu = document.getElementById('sort-menu');

    // By default, fetch movies sorted by added newest
    currentNode = document.getElementById('added-newest');
    fetchMovies(currentNode.id);

    // Fetch and display movies by sort option selected
    sortMenu.querySelectorAll('li').forEach(node => {
        node.addEventListener('click', (event) => {
            if (event.target === currentNode) {
                return;
            }
            currentNode.classList.remove('active');
            event.target.classList.add('active');
            currentNode = event.target;
            fetchMovies(currentNode.id);
        });
    });

    function fetchMovies(sort_by) {
        showLoading();
        console.log(`Fetching collection '${collection}' data for user sorted by ${sort_by}...`);
        fetch(`/api/collection/${collection}?sort=${encodeURIComponent(sort_by)}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (!data || data.length === 0 || data.error) {
                showError();
            }
            renderMoviesCount(data.total_count);
            renderMovies(data.movies);
        })
        .catch(error => console.log(error));
    }

    function renderMoviesCount(count) {
        let collectionVerb;
        if (collection === 'watched') {
            collectionVerb = 'watched';
        }
        else if (collection === 'watchlist') {
            collectionVerb = 'watchlisted';
        }
        else if (collection === 'favorites') {
            collectionVerb = 'favorited';
        }
        movieCountDiv.innerHTML = `You have ${collectionVerb} <b>${count} movies</b>.`;
    }

    function renderMovies(movies) {
        moviesDiv.innerHTML = '';
        movies.forEach(movie => {
            const movieDiv = document.createElement('div');
            movieDiv.classList.add('col-4', 'col-sm-3', 'col-md-2', 'text-center', 'mb-4');

            // Link to movie page
            const movieLink = document.createElement('a');
            movieLink.href = `/movie/${movie.tmdb_id}/`;

            // Add movie card with poster
            const movieCard = document.createElement('div');
            movieCard.classList.add('card', 'shadow', 'shadow-lg');
            const poster = document.createElement('img');
            if (movie.poster_path) {
                poster.src = `${tmdbImages}w500${movie.poster_path}`;
            }
            else {
                poster.src = `${staticImages}no_poster_92.jpg`;
            }
            poster.classList.add('card-img');
            poster.alt = movie.title;

            // Display title and release year overlay on hover
            const overlay = document.createElement('div');
            overlay.classList.add('card-img-overlay', 'overflow-y-auto');
            overlay.style.display = 'none';
            overlay.style.backgroundColor = 'black';
            overlay.style.opacity = 0.85;
            
            const title = document.createElement('h5');
            title.classList.add('card-title');
            title.style.color = 'white';
            title.innerHTML = movie.title;
            if (movie.release_date.length > 4) {
                title.innerHTML = `${movie.title} (${movie.release_date.slice(0, 4)})`;
            }
            overlay.append(title);

            movieCard.addEventListener('mouseover', () => {
                overlay.style.display = 'block';
            });
            movieCard.addEventListener('mouseout', () => {
                overlay.style.display = 'none';
            });

            movieCard.append(poster, overlay);
            movieLink.append(movieCard);
            movieDiv.append(movieLink);
            moviesDiv.append(movieDiv);
        });
        showMovies();
    }

    function showLoading() {
        errorDiv.style.display = 'none';
        moviesDiv.style.display = 'none';
        loadingDiv.style.display = 'block';
    }

    function showError() {
        loadingDiv.style.display = 'none';
        moviesDiv.style.display = 'none';
        errorDiv.style.display = 'block';
    }

    function showMovies() {
        loadingDiv.style.display = 'none';
        errorDiv.style.display = 'none';
        moviesDiv.style.display = 'flex';
    }
});