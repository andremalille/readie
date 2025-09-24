document.getElementById("category-search").addEventListener("input", function () {
    const filter = this.value.toLowerCase();
    const items = document.querySelectorAll("#category-checkboxes .category-item");

    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(filter) ? "block" : "none";
    });
});