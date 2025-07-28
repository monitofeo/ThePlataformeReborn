#version 330

uniform float time;
uniform vec2 resolution;

out vec4 fragColor;

float rand(vec2 co) {
    return fract(sin(dot(co.xy, vec2(12.989,78.233))) * 43758.5453);
}

void main() {
    vec2 uv = gl_FragCoord.xy / resolution;
    float drops = step(0.98, fract(uv.y * 40.0 + time * 5.0));
    float fade = smoothstep(1.0, 0.0, fract(uv.y * 40.0 + time * 5.0));

    vec3 color = mix(vec3(0.0, 0.0, 0.1), vec3(0.3, 0.6, 0.9), drops * fade);
    fragColor = vec4(color, 1.0);
}
