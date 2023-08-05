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
#ifndef __BLENDER_TOOLSETTINGS__H__
#define __BLENDER_TOOLSETTINGS__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ImagePaintSettings.h"
#include "blender_MeshStatVis.h"
#include "blender_ParticleEditSettings.h"
#include "blender_UnifiedPaintSettings.h"

namespace Blender {


    // ---------------------------------------------- //
    class ToolSettings
    {
    public:
        VPaint *vpaint;
        VPaint *wpaint;
        Sculpt *sculpt;
        UvSculpt *uvsculpt;
        float vgroup_weight;
        float doublimit;
        float normalsize;
        short automerge;
        short selectmode;
        char unwrapper;
        char uvcalc_flag;
        char uv_flag;
        char uv_selectmode;
        float uvcalc_margin;
        short autoik_chainlen;
        char gpencil_flags;
        char gpencil_src;
        char pad[4];
        ImagePaintSettings imapaint;
        ParticleEditSettings particle;
        float proportional_size;
        float select_thresh;
        short autokey_mode;
        short autokey_flag;
        char multires_subdiv_type;
        char pad3[1];
        short skgen_resolution;
        float skgen_threshold_internal;
        float skgen_threshold_external;
        float skgen_length_ratio;
        float skgen_length_limit;
        float skgen_angle_limit;
        float skgen_correlation_limit;
        float skgen_symmetry_limit;
        float skgen_retarget_angle_weight;
        float skgen_retarget_length_weight;
        float skgen_retarget_distance_weight;
        short skgen_options;
        char skgen_postpro;
        char skgen_postpro_passes;
        char skgen_subdivisions[3];
        char skgen_multi_level;
        Object *skgen_template;
        char bone_sketching;
        char bone_sketching_convert;
        char skgen_subdivision_number;
        char skgen_retarget_options;
        char skgen_retarget_roll;
        char skgen_side_string[8];
        char skgen_num_string[8];
        char edge_mode;
        char edge_mode_live_unwrap;
        char snap_mode;
        char snap_node_mode;
        char snap_uv_mode;
        short snap_flag;
        short snap_target;
        short proportional;
        short prop_mode;
        char proportional_objects;
        char proportional_mask;
        char proportional_action;
        char proportional_fcurve;
        char lock_markers;
        char pad4[5];
        char auto_normalize;
        char multipaint;
        char weightuser;
        char vgroupsubset;
        int use_uv_sculpt;
        int uv_sculpt_settings;
        int uv_sculpt_tool;
        int uv_relax_method;
        short sculpt_paint_settings;
        short pad5;
        int sculpt_paint_unified_size;
        float sculpt_paint_unified_unprojected_radius;
        float sculpt_paint_unified_alpha;
        UnifiedPaintSettings unified_paint_settings;
        MeshStatVis statvis;
    };
}


#endif//__BLENDER_TOOLSETTINGS__H__
