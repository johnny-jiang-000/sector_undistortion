void main(){
    vec2 a=cogl_tex_coord_in[0].xy;
    vec2 p=vec2(a.x*w_o-whalf_o,h_o+l-a.y*h_o);
    float r_2=p.x*p.x+p.y*p.y;
    float theta=atan(p.y/(p.x+0.00001))
    if(r_2>r_2min && r_2<r_2max && theta>theta_min && theta<theta_max){
        vec2 coord_in=vec2(PI_half+amax-theta)/da,(sqrt(r_2)-Rmin)/dr);
        coord_in.x/=w;
        coord_in.y/=h;
        cogl_color_out=cogl_color_in*texture2D(tex,coord_in);
    }
    else
        cogl_color_out=vec4(0.0,0.0,0.0,0.0);
}