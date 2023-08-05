/* Copyright (C) 2006 Charlie C
*
* This software is provided 'as-is', without any express or implied
* warranty.  In no event will the authors be held liable for any damages
* arising from the use of this software.
*
* Permission is granted to anyone to use this software for any purpose,
* including commercial applications, and to alter it and redistribute it
* freely, subject to the following restrictions:
*
* 1. The origin of this software must not be misrepresented; you must not
*    claim that you wrote the original software. If you use this software
*    in a product, an acknowledgment in the product documentation would be
*    appreciated but is not required.
* 2. Altered source versions must be plainly marked as such, and must not be
*    misrepresented as being the original software.
* 3. This notice may not be removed or altered from any source distribution.
*/
// Auto generated from makesdna dna.c
#ifndef __BLENDER_UNIFIEDPAINTSETTINGS__H__
#define __BLENDER_UNIFIEDPAINTSETTINGS__H__


// -------------------------------------------------- //
#include "blender_Common.h"

namespace Blender {


    // ---------------------------------------------- //
    class UnifiedPaintSettings
    {
    public:
        int size;
        float unprojected_radius;
        float alpha;
        float weight;
        vec3f rgb;
        vec3f secondary_rgb;
        int flag;
        float last_rake[2];
        float last_rake_angle;
        int last_stroke_valid;
        vec3f average_stroke_accum;
        int average_stroke_counter;
        float brush_rotation;
        float brush_rotation_sec;
        int anchored_size;
        float overlap_factor;
        char draw_inverted;
        char stroke_active;
        char draw_anchored;
        char do_linear_conversion;
        float anchored_initial_mouse[2];
        float pixel_radius;
        float size_pressure_value;
        float tex_mouse[2];
        float mask_tex_mouse[2];
        bInvalidHandle *colorspace;
    };
}


#endif//__BLENDER_UNIFIEDPAINTSETTINGS__H__
