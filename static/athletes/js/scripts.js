document.addEventListener('DOMContentLoaded', function() {
  var shareButton = document.getElementById('share-button');
  var formContainer = document.getElementById('share-form-container');
  var athleteSlug = shareButton.getAttribute('data-athlete-slug');

  shareButton.addEventListener('click', function() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/share/' + athleteSlug + '/', true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        formContainer.innerHTML = xhr.responseText;
      }
    };
    xhr.send();
  });



document.querySelector('a.like').addEventListener('click', function(e) {
    e.preventDefault();
    var likeButton = this;
    var url = likeButton.dataset.url;
    var id = likeButton.dataset.id;
    var action = likeButton.dataset.action;

    var options = {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin'
    };

    var formData = new FormData();
    formData.append('id', id);
    formData.append('action', action);
    options['body'] = formData;

    fetch(url, options)
        .then(response => response.json())
        .then(data => {
            if (data['status'] === 'ok') {
                var previousAction = likeButton.dataset.action;
                var action = previousAction === 'like' ? 'unlike' : 'like';
                likeButton.dataset.action = action;
                likeButton.innerHTML = action;

                var likeCount = document.querySelector('span.count .total');
                var totalLikes = parseInt(likeCount.innerHTML);
                likeCount.innerHTML = previousAction === 'like' ? totalLikes + 1 : totalLikes - 1;
            }
        });
});
});