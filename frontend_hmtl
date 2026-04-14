<script>
const box = document.getElementById("searchBox");
const results = document.getElementById("results");

let timeout = null;

box.addEventListener("input", () => {
    clearTimeout(timeout);

    timeout = setTimeout(async () => {
        const query = box.value;

        const res = await fetch(`/search?q=${query}`);
        const data = await res.json();

        results.innerHTML = "";

        data.forEach(book => {
            const div = document.createElement("div");
            div.className = "item";

            div.innerHTML = `
                <div class="title">${book.title}</div>
                <div class="author">${book.author}</div>
            `;

            results.appendChild(div);
        });

    }, 150); // small delay (prevents spam)
});
</script>