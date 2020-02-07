void main(){
    vec2 a=cogl_tex_coord_in[0].xy;
    vec2 p=vec2(a.x*w_o-whalf_o,h_o+l-a.y*h_o);
    float r_2=p.x*p.x+p.y*p.y;
    float sine_2=p.y*p.y/r_2;
    if(r_2>r_2min && r_2<r_2max && sine_2>sine_2min && sine_2<sine_2max){
        vec2 coord_in=vec2(atan(p.y/p.x),(sqrt(r_2)-Rmin)/dr);
        cogl_color_out=cogl_color_in*texture2D(tex,coord);
    }
    else
        cogl_color_out=vec4(0.0,0.0,0.0,0.0);
}