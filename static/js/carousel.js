const track = document.querySelector('.carousel__track');
const slides = Array.from(track.children);
const nextButton = document.querySelector('.carousel__button--right');
const prevButton = document.querySelector('.carousel__button--left');

const slideWidth = slides[0].getBoundingClientRect().width;

const arrangeSlides = (slide, index) => {
    slide.style.left = slideWidth * index + 'px';
}
slides.forEach(arrangeSlides)

const moveToSlide = (track, currentSlide, targetSlide) => {
    track.style.transform = 'translateX(-' + targetSlide.style.left + ')';
    currentSlide.classList.remove('current-slide');
    targetSlide.classList.add('current-slide');
};

const currentSlide = track.querySelector('.current-slide');
let nextSlide = currentSlide.nextElementSibling;

if (!nextSlide) {
    nextSlide = slides[0];
}

moveToSlide(track, currentSlide, nextSlide);
document.querySelector('.carousel__track').style.transition = 'transform 250ms ease-in';

nextButton.addEventListener('click', e => {
    const currentSlide = track.querySelector('.current-slide');
    let nextSlide = currentSlide.nextElementSibling;

    if (!nextSlide) {
        nextSlide = slides[0];
    }

    moveToSlide(track, currentSlide, nextSlide);
})

prevButton.addEventListener('click', e => {
    const currentSlide = track.querySelector('.current-slide');
    let prevSlide = currentSlide.previousElementSibling;

    if (!prevSlide) {
        prevSlide = slides[slides.length - 1];
    }
    console.log(prevSlide)
    moveToSlide(track, currentSlide, prevSlide);
})