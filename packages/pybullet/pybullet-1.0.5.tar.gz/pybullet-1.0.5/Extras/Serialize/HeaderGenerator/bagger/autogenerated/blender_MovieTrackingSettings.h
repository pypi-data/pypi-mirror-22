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
#ifndef __BLENDER_MOVIETRACKINGSETTINGS__H__
#define __BLENDER_MOVIETRACKINGSETTINGS__H__


// -------------------------------------------------- //
#include "blender_Common.h"

namespace Blender {


    // ---------------------------------------------- //
    class MovieTrackingSettings
    {
    public:
        int flag;
        short default_motion_model;
        short default_algorithm_flag;
        float default_minimum_correlation;
        short default_pattern_size;
        short default_search_size;
        short default_frames_limit;
        short default_margin;
        short default_pattern_match;
        short default_flag;
        float default_weight;
        short motion_flag;
        short speed;
        int keyframe1;
        int keyframe2;
        int reconstruction_flag;
        short refine_camera_intrinsics;
        short pad2;
        float dist;
        int clean_frames;
        int clean_action;
        float clean_error;
        float object_distance;
        int pad3;
    };
}


#endif//__BLENDER_MOVIETRACKINGSETTINGS__H__
