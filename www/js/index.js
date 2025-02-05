
window.onFontStyleChange = fontStyle => {
    let fontFamily
    if (fontStyle === 'SquareDot') {
        fontFamily = 'VerticalSans-SquareDot, sans-serif'
    } else if (fontStyle === 'CircleDot') {
        fontFamily = 'VerticalSans-CircleDot, sans-serif'
    } else {
        fontFamily = 'VerticalSans, sans-serif'
    }
    document.getElementById('title').style.fontFamily = fontFamily
    document.getElementById('input-box').style.fontFamily = fontFamily
}
