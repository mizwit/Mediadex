document.addEventListener('DOMContentLoaded', () => {

    const showProfile = document.getElementById('show-profile');
    const editProfile = document.getElementById('edit-profile');
    const editBtn = document.getElementById('edit-btn');
    const saveBtn = document.getElementById('save-btn');

    // Display edit profile form
    editBtn.addEventListener('click', () => setDisplay({
        showDisplay: 'none',
        editDisplay: 'block'
    }));

    // Display user profile
    saveBtn.addEventListener('click', () => setDisplay({
        showDisplay: 'block',
        editDisplay: 'none'
    }));

    function setDisplay({showDisplay, editDisplay}) {
        showProfile.style.display = showDisplay;
        editBtn.style.display = showDisplay;
        editProfile.style.display = editDisplay;
        saveBtn.style.display = editDisplay;
    }
});