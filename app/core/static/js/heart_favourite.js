document.addEventListener("DOMContentLoaded", function () {
    const heartButton = document.getElementById("heartButton");

    heartButton.addEventListener("click", function (event) {
        event.preventDefault();
        this.classList.toggle("active");

        if (this.classList.contains("active")) {
            this.setAttribute("title", "Remove from favourites");
        } else {
            this.setAttribute("title", "Add to favourites");
        }
    });
});