// Set up CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', () => {
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const detailsDiv = document.getElementById('details');
    const movieId = detailsDiv.dataset.movieId;

    // Fetch details using movie id
    fetchDetails();

    function fetchDetails() {
        console.log(`Getting details for movie id '${movieId}'...`);
        fetch(`/api/tmdb/movie/${movieId}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (!data || data.length === 0 || data.success === false) {
                showError();
                return;
            }
            renderDetails(data);
        })
        .catch(error => console.log(error));
    }

    function renderDetails(data) {
        // Define basic structure
        const row = document.createElement('div');
        const col1 = document.createElement('div');
        const col2 = document.createElement('div');
        row.classList.add('row');
        col1.classList.add('col-12', 'col-sm-6', 'col-md-4', 'col-lg-3', 'd-flex', 'flex-column', 'justify-content-start', 'align-items-center');
        col2.classList.add('col-12', 'col-sm-6', 'col-md-8', 'col-lg-9', 'd-flex', 'flex-column', 'justify-content-between', 'align-items-start');

        // Add backdrop image
        const backdrop = document.getElementById('backdrop');
        if (data.backdrop_path) {
            backdrop.src = `${tmdbImages}w1280/${data.backdrop_path}`;
        }
        else {
            backdrop.src = `${staticImages}no_backdrop_1280.jpg`;
        }
        backdrop.classList.add('img-fluid');
        backdrop.alt = data.title + ' Backdrop';

        // Add poster image
        const posterDiv = document.createElement('div');
        posterDiv.classList.add('mb-2');
        const poster = document.createElement('img');
        poster.id = 'poster';
        if (data.poster_path) {
            poster.src = `${tmdbImages}w500${data.poster_path}`;
        }
        else {
            poster.src = `${staticImages}no_poster_185.jpg`;
        }
        poster.classList.add('img-fluid', 'rounded')
        poster.alt = data.title + ' Poster';
        poster.width = 185;
        poster.height = 278;
        posterDiv.appendChild(poster);

        // Add user actions
        const actionsDiv = document.createElement('div');
        actionsDiv.classList.add('card', 'mb-2');
        const actions = document.createElement('ul');
        actions.classList.add('list-group', 'list-group-flush');

        if (isAuthenticated) {
            const watchedAction = document.createElement('li');
            const watchlistAction = document.createElement('li');
            const favoritesAction = document.createElement('li');

            // Add to or Remove from Watched
            const watchedAdd = document.createElement('button');
            watchedAdd.classList.add('btn', 'btn-secondary', 'fw-bold', 'hoverable');
            watchedAdd.innerHTML = 'Add to Watched <i class="bi bi-collection-play ms-1"><i>';
            watchedAdd.addEventListener('click', () => {
                updateMovieStatus('watched', false);
                watchedAdd.style.display = 'none';
                watchedRemove.style.display = 'block';
            });
            const watchedRemove = document.createElement('button');
            watchedRemove.classList.add('btn', 'btn-warning', 'fw-bold', 'hoverable');
            watchedRemove.innerHTML = 'Remove Watched <i class="bi bi-collection-play-fill ms-1"><i>';
            watchedRemove.addEventListener('click', () => {
                updateMovieStatus('watched', true);
                watchedRemove.style.display = 'none';
                watchedAdd.style.display = 'block';
            });
            watchedAction.append(watchedAdd, watchedRemove);
            
            // Add to or Remove from Watchlist
            const watchlistAdd = document.createElement('button');
            watchlistAdd.classList.add('btn', 'btn-secondary', 'fw-bold', 'hoverable');
            watchlistAdd.innerHTML = 'Add to Watchlist <i class="bi bi-bookmark-plus ms-1"><i>';
            watchlistAdd.addEventListener('click', () => {
                updateMovieStatus('watchlist', false);
                watchlistAdd.style.display = 'none';
                watchlistRemove.style.display = 'block';
            });
            const watchlistRemove = document.createElement('button');
            watchlistRemove.classList.add('btn', 'btn-warning', 'fw-bold', 'hoverable');
            watchlistRemove.innerHTML = 'Remove Watchlist <i class="bi bi-bookmark-plus-fill ms-1"><i>';
            watchlistRemove.addEventListener('click', () => {
                updateMovieStatus('watchlist', true);
                watchlistRemove.style.display = 'none';
                watchlistAdd.style.display = 'block';
            });
            watchlistAction.append(watchlistAdd, watchlistRemove);

            // Add to or Remove from Favorites
            const favoritesAdd = document.createElement('div');
            favoritesAdd.classList.add('btn', 'btn-secondary', 'fw-bold', 'hoverable');
            favoritesAdd.innerHTML = 'Add to Favorites <i class="bi bi-heart ms-1"><i>';
            favoritesAdd.addEventListener('click', () => {
                updateMovieStatus('favorites', false);
                favoritesAdd.style.display = 'none';
                favoritesRemove.style.display = 'block';
            });
            const favoritesRemove = document.createElement('div');
            favoritesRemove.classList.add('btn', 'btn-warning', 'fw-bold', 'hoverable');
            favoritesRemove.innerHTML = 'Remove Favorites <i class="bi bi-heart-fill ms-1"><i>';
            favoritesRemove.addEventListener('click', () => {
                updateMovieStatus('favorites', true);
                favoritesRemove.style.display = 'none';
                favoritesAdd.style.display = 'block';
            });
            favoritesAction.append(favoritesAdd, favoritesRemove);

            // Toggle actions visiblity based on current movie status in various collections
            console.log(`Getting status for movie id '${movieId}'...`);
            fetch(`/api/status/movie/${movieId}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if (data.watched) {
                    watchedAdd.style.display = 'none';
                    watchedRemove.style.display = 'flex';
                }
                else {
                    watchedRemove.style.display = 'none';
                    watchedAdd.style.display = 'flex';
                }
                if (data.watchlist) {
                    watchlistAdd.style.display = 'none';
                    watchlistRemove.style.display = 'flex';
                }
                else {
                    watchlistRemove.style.display = 'none';
                    watchlistAdd.style.display = 'flex';
                }
                if (data.favorites) {
                    favoritesAdd.style.display = 'none';
                    favoritesRemove.style.display = 'flex';
                }
                else {
                    favoritesRemove.style.display = 'none';
                    favoritesAdd.style.display = 'flex';
                }
            })
            .catch(error => console.log(error));
            actions.append(watchedAction, watchlistAction, favoritesAction);
        }
        else {
            // If no user, prompt to sign in
            const loginAction = document.createElement('li');            
            loginText = document.createElement('div');
            loginText.classList.add('me-auto');
            loginText.innerHTML = '<div class="fw-bold">Login</div>Sign in to add this to your collection.';
            loginLink = document.createElement('a');
            loginLink.classList.add('icon-link', 'icon-link-hover')
            loginLink.href = `/accounts/login/?next=${window.location.pathname}`;
            loginLink.innerHTML = '<i class="bi bi-arrow-right"></i>';
            loginAction.append(loginText, loginLink);
            actions.append(loginAction);
        }
        actions.childNodes.forEach(action => {
            action.classList.add('list-group-item', 'd-flex', 'justify-content-center', 'align-items-stretch', 'overflow-x-auto');
        });
        actionsDiv.appendChild(actions);

        // Add movie description
        const descriptionDiv = document.createElement('div');
        const title = document.createElement('h1');
        if (data.release_date) {
            title.innerHTML = `${data.title}
            <small class="text-body-secondary">(${data.release_date.slice(0, 4)})</small>`;    
        }
        else {
            title.innerHTML = data.title;
        }
        descriptionDiv.append(title);
        if (data.original_title != data.title) {
            const original_title = document.createElement('h4');
            original_title.classList.add('text-body-secondary');
            original_title.innerHTML = data.original_title;
            descriptionDiv.append(original_title);
        }
        if (data.tagline) {
            const tagline = document.createElement('p');
            tagline.classList.add('font-monospace', 'fw-semibold');
            tagline.style.marginBottom = 0;
            tagline.innerHTML = data.tagline;
            descriptionDiv.append(tagline);
        }
        const overview = document.createElement('p');
        overview.innerHTML = data.overview;
        descriptionDiv.append(overview);

        // Add movie stats (votes, genres)
        const statsDiv = document.createElement('div');
        if (data.vote_average && data.vote_count) {
            const votesDiv = document.createElement('div');
            votesDiv.classList.add('hstack', 'gap-2', 'mb-2');

            const tmdbLogo = document.createElement('img');
            tmdbLogo.src = `${staticImages}tmdb_logo.svg`;
            tmdbLogo.alt = 'TMDB';
            tmdbLogo.height = 10;

            const voteAverage = document.createElement('div');
            voteAverage.classList.add('font-monospace');
            voteAverage.innerHTML = `Score ${data.vote_average.toFixed(1)}/10`;

            const voteCount = document.createElement('div');
            voteCount.classList.add('text-body-secondary');
            voteCount.innerHTML = `(${data.vote_count})`;

            votesDiv.append(tmdbLogo, voteAverage, voteCount);
            statsDiv.append(votesDiv);
        }
        if (data.genres && data.genres.length > 0) {
            const genresDiv = document.createElement('div');
            genresDiv.classList.add('hstack', 'gap-3', 'mb-2');
            let genres = data.genres;
            if (data.genres.length > 3){
                genres = data.genres.slice(2);
            }
            genres.forEach(item => {
                const genre = document.createElement('button');
                genre.classList.add('btn', 'rounded', 'border', 'hoverable')
                genre.innerHTML = item.name;
                genresDiv.append(genre);
            });
            statsDiv.append(genresDiv);
        }

        // Construct the components and add to details
        col1.append(posterDiv, actionsDiv);
        col2.append(descriptionDiv, statsDiv);
        row.append(col1, col2);
        detailsDiv.append(row);
        
        showDetails();
    }

    function showError() {
        loadingDiv.style.display = 'none';
        detailsDiv.style.display = 'none';
        errorDiv.style.display = 'block';
    }

    function showDetails() {
        errorDiv.style.display = 'none';
        loadingDiv.style.display = 'none';
        detailsDiv.style.display = 'block';
    }

    function updateMovieStatus(collection, currentStatus) {
        // Update movie status in collection based on current status
        console.log(`Updating movie id '${movieId}' status in '${collection}' from ${currentStatus} to ${!currentStatus}...`);
        fetch(`/api/update/movie/${movieId}`, {
            method: 'PUT',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin',
            body: JSON.stringify({
                collection: collection,
                current_status: currentStatus
            })
        })
        .catch(error => console.log(error));
    }
});