var elements = document.getElementsByTagName("input");
for (var inp of elements) {
    if (inp.type === "radio")
        inp.checked = false;
        }

