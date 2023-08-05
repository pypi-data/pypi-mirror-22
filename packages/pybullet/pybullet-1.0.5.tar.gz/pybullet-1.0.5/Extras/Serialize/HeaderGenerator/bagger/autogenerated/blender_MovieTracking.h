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
#ifndef __BLENDER_MOVIETRACKING__H__
#define __BLENDER_MOVIETRACKING__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ListBase.h"
#include "blender_MovieTrackingCamera.h"
#include "blender_MovieTrackingDopesheet.h"
#include "blender_MovieTrackingReconstruction.h"
#include "blender_MovieTrackingSettings.h"
#include "blender_MovieTrackingStabilization.h"

namespace Blender {


    // ---------------------------------------------- //
    class MovieTracking
    {
    public:
        MovieTrackingSettings settings;
        MovieTrackingCamera camera;
        ListBase tracks;
        ListBase plane_tracks;
        MovieTrackingReconstruction reconstruction;
        MovieTrackingStabilization stabilization;
        MovieTrackingTrack *act_track;
        MovieTrackingPlaneTrack *act_plane_track;
        ListBase objects;
        int objectnr;
        int tot_object;
        MovieTrackingStats *stats;
        MovieTrackingDopesheet dopesheet;
    };
}


#endif//__BLENDER_MOVIETRACKING__H__
