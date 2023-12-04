
async function getNotebook(url) {
    const response = await fetch(url);
    return await response.json();
}

async function renderNotebookAsync(selector, url) {
    var $holder = document.querySelector(selector);

    const nb = await getNotebook(url);

    while ($holder.hasChildNodes()) {
        $holder.removeChild($holder.lastChild);
    }
    $holder.innerHTML = nb;
}

function renderNotebook(selector, url) {
    renderNotebookAsync(selector, url)
        .then(() => {
            console.log("Loaded notebook.");
        });
}
