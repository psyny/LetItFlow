export class ColorTools {
    static RgbToFilterString(rgb) {
        if (!Array.isArray(rgb) || rgb.length !== 3 || !rgb.every(c => c >= 0 && c <= 255)) {
            throw new Error("Input must be an array of three numbers between 0 and 255.");
        }
    
        const [r, g, b] = rgb;
    
        // Normalize RGB to a range of 0 to 1
        const rNorm = r / 255;
        const gNorm = g / 255;
        const bNorm = b / 255;
    
        // Calculate perceived brightness (luminance)
        const brightness = 0.299 * rNorm + 0.587 * gNorm + 0.114 * bNorm;
        const cssBrightness = brightness * 100; // Convert to percentage
    
        // Calculate saturation using max and min of normalized values
        const max = Math.max(rNorm, gNorm, bNorm);
        const min = Math.min(rNorm, gNorm, bNorm);
        const saturation = max === 0 ? 0 : ((max - min) / max) * 100;
    
        // Calculate hue (angle in degrees)
        let hue = 0;
        if (max === min) {
            hue = 0; // No hue if max and min are equal
        } else if (max === rNorm) {
            hue = (60 * ((gNorm - bNorm) / (max - min)) + 360) % 360;
        } else if (max === gNorm) {
            hue = (60 * ((bNorm - rNorm) / (max - min)) + 120) % 360;
        } else if (max === bNorm) {
            hue = (60 * ((rNorm - gNorm) / (max - min)) + 240) % 360;
        }
    
        // Construct the filter string with improved logic
        const filter = `filter: brightness(${cssBrightness.toFixed(0)}%) saturate(${(saturation + 100).toFixed(0)}%) hue-rotate(${hue.toFixed(0)}deg);`;
    
        return filter;
    }
}