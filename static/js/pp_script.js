var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    // Deactivate all collapsibles
    for (var j = 0; j < coll.length; j++) {
      if (coll[j] !== this) {
        coll[j].classList.remove("active");
        var content = coll[j].nextElementSibling;
        content.style.maxHeight = null;
      }
    }

    // Toggle active class and adjust max-height for the clicked collapsible
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight) {
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}

document.getElementById("topLink").addEventListener("click", function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});


// Function to set up click event listener for each trigger text
function setupClickListener(triggerTextId, targetButtonId, targetSectionId) {
    document.getElementById(triggerTextId).addEventListener("click", function() {
        // Trigger click event on the target button
        document.getElementById(targetButtonId).click();

        // Scroll to the target section above the button
        const targetSection = document.getElementById(targetSectionId);
        const topOffset = targetSection.getBoundingClientRect().top + window.scrollY;
        window.scrollTo({ top: topOffset - 150, behavior: 'smooth' });
    });
}

// Set up click event listeners for each text-button pair
setupClickListener("triggerText1", "targetButton1", "targetSection1");
setupClickListener("triggerText2", "targetButton2", "targetSection2");
setupClickListener("triggerText3", "targetButton3", "targetSection3");
setupClickListener("triggerText4", "targetButton4", "targetSection4");
setupClickListener("triggerText5", "targetButton5", "targetSection5");
setupClickListener("triggerText6", "targetButton6", "targetSection6");
setupClickListener("triggerText7", "targetButton7", "targetSection7");
setupClickListener("triggerText8", "targetButton8", "targetSection8");
setupClickListener("triggerText9", "targetButton9", "targetSection9");



