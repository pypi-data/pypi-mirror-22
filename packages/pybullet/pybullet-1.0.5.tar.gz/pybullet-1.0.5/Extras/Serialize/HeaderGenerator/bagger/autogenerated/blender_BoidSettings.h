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
#ifndef __BLENDER_BOIDSETTINGS__H__
#define __BLENDER_BOIDSETTINGS__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_ListBase.h"

namespace Blender {


    // ---------------------------------------------- //
    class BoidSettings
    {
    public:
        int options;
        int last_state_id;
        float landing_smoothness;
        float height;
        float banking;
        float pitch;
        float health;
        float aggression;
        float strength;
        float accuracy;
        float range;
        float air_min_speed;
        float air_max_speed;
        float air_max_acc;
        float air_max_ave;
        float air_personal_space;
        float land_jump_speed;
        float land_max_speed;
        float land_max_acc;
        float land_max_ave;
        float land_personal_space;
        float land_stick_force;
        ListBase states;
    };
}


#endif//__BLENDER_BOIDSETTINGS__H__
