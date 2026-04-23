document.getElementById("searchBar").addEventListener("keyup", function(){
    let filter = this.value.trim();
    let rows = document.querySelectorAll("#TicketsTable tbody tr");

    rows.array.forEach(row => {
        let ticketID = row.cells[0].innerText;
        if (filter == "" || ticketID.includes(filter)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
});