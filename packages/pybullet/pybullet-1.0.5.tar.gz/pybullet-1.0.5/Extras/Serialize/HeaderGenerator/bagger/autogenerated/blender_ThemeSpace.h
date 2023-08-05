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
#ifndef __BLENDER_THEMESPACE__H__
#define __BLENDER_THEMESPACE__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_uiGradientColors.h"
#include "blender_uiPanelColors.h"

namespace Blender {


    // ---------------------------------------------- //
    class ThemeSpace
    {
    public:
        char back[4];
        char title[4];
        char text[4];
        char text_hi[4];
        char header[4];
        char header_title[4];
        char header_text[4];
        char header_text_hi[4];
        char tab_active[4];
        char tab_inactive[4];
        char tab_back[4];
        char tab_outline[4];
        char button[4];
        char button_title[4];
        char button_text[4];
        char button_text_hi[4];
        char list[4];
        char list_title[4];
        char list_text[4];
        char list_text_hi[4];
        uiPanelColors panelcolors;
        uiGradientColors gradients;
        char shade1[4];
        char shade2[4];
        char hilite[4];
        char grid[4];
        char view_overlay[4];
        char wire[4];
        char wire_edit[4];
        char select[4];
        char lamp[4];
        char speaker[4];
        char empty[4];
        char camera[4];
        char active[4];
        char group[4];
        char group_active[4];
        char transform[4];
        char vertex[4];
        char vertex_select[4];
        char vertex_unreferenced[4];
        char edge[4];
        char edge_select[4];
        char edge_seam[4];
        char edge_sharp[4];
        char edge_facesel[4];
        char edge_crease[4];
        char face[4];
        char face_select[4];
        char face_dot[4];
        char extra_edge_len[4];
        char extra_edge_angle[4];
        char extra_face_angle[4];
        char extra_face_area[4];
        char normal[4];
        char vertex_normal[4];
        char loop_normal[4];
        char bone_solid[4];
        char bone_pose[4];
        char bone_pose_active[4];
        char strip[4];
        char strip_select[4];
        char cframe[4];
        char time_keyframe[4];
        char time_gp_keyframe[4];
        char freestyle_edge_mark[4];
        char freestyle_face_mark[4];
        char nurb_uline[4];
        char nurb_vline[4];
        char act_spline[4];
        char nurb_sel_uline[4];
        char nurb_sel_vline[4];
        char lastsel_point[4];
        char handle_free[4];
        char handle_auto[4];
        char handle_vect[4];
        char handle_align[4];
        char handle_auto_clamped[4];
        char handle_sel_free[4];
        char handle_sel_auto[4];
        char handle_sel_vect[4];
        char handle_sel_align[4];
        char handle_sel_auto_clamped[4];
        char ds_channel[4];
        char ds_subchannel[4];
        char keytype_keyframe[4];
        char keytype_extreme[4];
        char keytype_breakdown[4];
        char keytype_jitter[4];
        char keytype_keyframe_select[4];
        char keytype_extreme_select[4];
        char keytype_breakdown_select[4];
        char keytype_jitter_select[4];
        char keyborder[4];
        char keyborder_select[4];
        char console_output[4];
        char console_input[4];
        char console_info[4];
        char console_error[4];
        char console_cursor[4];
        char console_select[4];
        char vertex_size;
        char outline_width;
        char facedot_size;
        char noodle_curving;
        char syntaxl[4];
        char syntaxs[4];
        char syntaxb[4];
        char syntaxn[4];
        char syntaxv[4];
        char syntaxc[4];
        char syntaxd[4];
        char syntaxr[4];
        char nodeclass_output[4];
        char nodeclass_filter[4];
        char nodeclass_vector[4];
        char nodeclass_texture[4];
        char nodeclass_shader[4];
        char nodeclass_script[4];
        char nodeclass_pattern[4];
        char nodeclass_layout[4];
        char movie[4];
        char movieclip[4];
        char mask[4];
        char image[4];
        char scene[4];
        char audio[4];
        char effect[4];
        char transition[4];
        char meta[4];
        char editmesh_active[4];
        char handle_vertex[4];
        char handle_vertex_select[4];
        char handle_vertex_size;
        char clipping_border_3d[4];
        char marker_outline[4];
        char marker[4];
        char act_marker[4];
        char sel_marker[4];
        char dis_marker[4];
        char lock_marker[4];
        char bundle_solid[4];
        char path_before[4];
        char path_after[4];
        char camera_path[4];
        char hpad[2];
        char gp_vertex_size;
        char gp_vertex[4];
        char gp_vertex_select[4];
        char preview_back[4];
        char preview_stitch_face[4];
        char preview_stitch_edge[4];
        char preview_stitch_vert[4];
        char preview_stitch_stitchable[4];
        char preview_stitch_unstitchable[4];
        char preview_stitch_active[4];
        char uv_shadow[4];
        char uv_others[4];
        char match[4];
        char selected_highlight[4];
        char skin_root[4];
        char anim_active[4];
        char anim_non_active[4];
        char nla_tweaking[4];
        char nla_tweakdupli[4];
        char nla_transition[4];
        char nla_transition_sel[4];
        char nla_meta[4];
        char nla_meta_sel[4];
        char nla_sound[4];
        char nla_sound_sel[4];
        char info_selected[4];
        char info_selected_text[4];
        char info_error[4];
        char info_error_text[4];
        char info_warning[4];
        char info_warning_text[4];
        char info_info[4];
        char info_info_text[4];
        char info_debug[4];
        char info_debug_text[4];
        char paint_curve_pivot[4];
        char paint_curve_handle[4];
        char metadatabg[4];
        char metadatatext[4];
    };
}


#endif//__BLENDER_THEMESPACE__H__
