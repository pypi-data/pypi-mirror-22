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
#ifndef __BLENDER_SCENE__H__
#define __BLENDER_SCENE__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_AudioData.h"
#include "blender_ColorManagedColorspaceSettings.h"
#include "blender_ColorManagedDisplaySettings.h"
#include "blender_ColorManagedViewSettings.h"
#include "blender_DisplaySafeAreas.h"
#include "blender_GameData.h"
#include "blender_GameFraming.h"
#include "blender_ID.h"
#include "blender_ListBase.h"
#include "blender_PhysicsSettings.h"
#include "blender_RenderData.h"
#include "blender_UnitSettings.h"

namespace Blender {


    // ---------------------------------------------- //
    class Scene
    {
    public:
        ID id;
        AnimData *adt;
        Object *camera;
        World *world;
        Scene *set;
        ListBase base;
        Base *basact;
        Object *obedit;
        vec3f cursor;
        vec3f twcent;
        vec3f twmin;
        vec3f twmax;
        int lay;
        int layact;
        int lay_updated;
        short flag;
        char use_nodes;
        char pad[1];
        bNodeTree *nodetree;
        Editing *ed;
        ToolSettings *toolsettings;
        bInvalidHandle *stats;
        DisplaySafeAreas safe_areas;
        RenderData r;
        AudioData audio;
        ListBase markers;
        ListBase transform_spaces;
        void *sound_scene;
        void *playback_handle;
        void *sound_scrub_handle;
        void *speaker_handles;
        void *fps_info;
        bInvalidHandle *depsgraph;
        void *pad1;
        bInvalidHandle *theDag;
        short dagflags;
        short recalc;
        int active_keyingset;
        ListBase keyingsets;
        GameFraming framing;
        GameData gm;
        UnitSettings unit;
        bGPdata *gpd;
        PhysicsSettings physics_settings;
        MovieClip *clip;
        bInvalidHandle customdata_mask;
        bInvalidHandle customdata_mask_modal;
        ColorManagedViewSettings view_settings;
        ColorManagedDisplaySettings display_settings;
        ColorManagedColorspaceSettings sequencer_colorspace_settings;
        RigidBodyWorld *rigidbody_world;
    };
}


#endif//__BLENDER_SCENE__H__
