/**
 * Demo video: cover image + play button, click to play
 */
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.video-wrapper').forEach(function (wrapper) {
    var cover = wrapper.querySelector('.video-cover');
    var video = wrapper.querySelector('video');
    if (!cover || !video) return;

    var poster = cover.getAttribute('data-poster');
    if (poster) {
      cover.style.backgroundImage = "url('" + poster + "')";
    }

    function playVideo() {
      var src = video.getAttribute('data-src');
      if (src) {
        video.src = src;
        video.removeAttribute('data-src');
      }
      video.classList.add('playing');
      cover.classList.add('hidden');
      video.controls = true;
      video.play();
    }

    cover.addEventListener('click', playVideo);
    wrapper.querySelector('.video-play-btn').addEventListener('click', function (e) {
      e.stopPropagation();
      playVideo();
    });
  });
});
