
document.addEventListener("DOMContentLoaded", function () {
    function toggleZusatzInfo(event) {
        let selectedRadio = event.target; // Der geklickte Radio-Button
        let targetIds = selectedRadio.dataset.target.split(","); // Mehrere IDs

        targetIds.forEach(targetId => {
            let extraField = document.getElementById(targetId.trim());
            if (targetId.trim() == "div_id_4-child_development_no") {
                if (extraField) {
                    extraField.style.display = selectedRadio.value === "False" ? "block" : "none";
                }
            }
            else {
                if (extraField) {
                    extraField.style.display = selectedRadio.value === "True" ? "block" : "none";
                }
            }
        });
    }

    // Event Listener für alle Ja/Nein-Radiobuttons mit data-target
    document.querySelectorAll('input[type="radio"][data-target]').forEach(function (radio) {
        radio.addEventListener("change", toggleZusatzInfo);
    });


    // Beim Laden: Alle Zusatzfelder standardmäßig verstecken, falls kein "Ja" ausgewählt wurde
    document.querySelectorAll('input[type="radio"][data-target]').forEach(function (radio) {
        let targetIds = radio.dataset.target.split(",");
        let isChecked = document.querySelector(`input[name="${radio.name}"]:checked`);

        targetIds.forEach(targetId => {
            let extraField = document.getElementById(targetId.trim());
            if (extraField) {
                extraField.style.display = isChecked && isChecked.value === "True" ? "block" : "none";
            }
        });
    });
});

