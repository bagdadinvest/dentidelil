document.addEventListener("DOMContentLoaded", function () {
    // Create the floating button
    var floatingButton = document.createElement('button');
    floatingButton.type = 'button';
    floatingButton.innerText = 'Choose AI Template';
    floatingButton.classList.add('floating-button');

    // Append the floating button to the body
    document.body.appendChild(floatingButton);

    // Handle button click to open snippet chooser
    floatingButton.addEventListener('click', function () {
        var snippetField = document.querySelector('[name="ai_content_template"]');
        if (snippetField) {
            snippetField.click();  // Simulate the click on the snippet chooser
        }
    });

    // You can also attach an event listener to automatically fill fields after snippet selection as done earlier.
    var snippetField = document.querySelector('[name="ai_content_template"]');
    if (snippetField) {
        snippetField.addEventListener('change', function () {
            var snippetId = snippetField.value;
            if (snippetId) {
                fetch(`/admin/get-snippet-content/${snippetId}/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.content) {
                        var titleField = document.querySelector('#id_title');
                        var bodyField = document.querySelector('[data-panel-label="Body"] .input');

                        titleField.value = data.content.title;
                        var richTextEditor = bodyField.querySelector('.rich-text');
                        if (richTextEditor) {
                            richTextEditor.innerHTML = data.content.body;
                        }
                    } else {
                        alert("Failed to fetch snippet content.");
                    }
                })
                .catch(error => console.log('Error fetching snippet content:', error));
            }
        });
    }
});
