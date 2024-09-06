document.getElementById("reviewForm").addEventListener("submit", function (event) {
    event.preventDefault();
    var addReviewUrl = 
    document.getElementById("reviewForm").dataset.addReviewUrl;
    var currentUser = document.querySelector('input[name="user"]').value;
    var currentDate = new Date().toISOString().split('T')[0];
    var formData = new FormData(this);

    formData.set('user', currentUser);
    formData.set('review_date', currentDate);
    for (var pair of formData.entries()) {
    console.log(pair[0] + ', ' + pair[1]);
    }
    fetch(addReviewUrl, {
    method: 'POST',
    body: formData,
    })
    .then(response => response.json())
    .then(data => {
    if (data.success) {
    alert("Отзыв успешно добавлен!");
    window.location.reload();
    } else {
    alert("Ошибка при добавлении отзыва ");
    }
    })
    .catch(error => {
    alert("Ошибка при отправке запроса");
    });
});