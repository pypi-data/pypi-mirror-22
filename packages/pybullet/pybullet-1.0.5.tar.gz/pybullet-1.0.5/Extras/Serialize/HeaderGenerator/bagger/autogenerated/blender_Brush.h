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
#ifndef __BLENDER_BRUSH__H__
#define __BLENDER_BRUSH__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_BrushClone.h"
#include "blender_ID.h"
#include "blender_MTex.h"

namespace Blender {


    // ---------------------------------------------- //
    class Brush
    {
    public:
        ID id;
        BrushClone clone;
        CurveMapping *curve;
        MTex mtex;
        MTex mask_mtex;
        Brush *toggle_brush;
        bInvalidHandle *icon_imbuf;
        PreviewImage *preview;
        ColorBand *gradient;
        PaintCurve *paint_curve;
        char icon_filepath[1024];
        float normal_weight;
        short blend;
        short ob_mode;
        float weight;
        int size;
        int flag;
        int mask_pressure;
        float jitter;
        int jitter_absolute;
        int overlay_flags;
        int spacing;
        int smooth_stroke_radius;
        float smooth_stroke_factor;
        float rate;
        vec3f rgb;
        float alpha;
        vec3f secondary_rgb;
        int sculpt_plane;
        float plane_offset;
        int flag2;
        int gradient_spacing;
        int gradient_stroke_mode;
        int gradient_fill_mode;
        char sculpt_tool;
        char vertexpaint_tool;
        char imagepaint_tool;
        char mask_tool;
        float autosmooth_factor;
        float crease_pinch_factor;
        float plane_trim;
        float height;
        float texture_sample_bias;
        int texture_overlay_alpha;
        int mask_overlay_alpha;
        int cursor_overlay_alpha;
        float unprojected_radius;
        float sharp_threshold;
        int blur_kernel_radius;
        int blur_mode;
        float fill_threshold;
        vec3f add_col;
        vec3f sub_col;
        float stencil_pos[2];
        float stencil_dimension[2];
        float mask_stencil_pos[2];
        float mask_stencil_dimension[2];
    };
}


#endif//__BLENDER_BRUSH__H__
