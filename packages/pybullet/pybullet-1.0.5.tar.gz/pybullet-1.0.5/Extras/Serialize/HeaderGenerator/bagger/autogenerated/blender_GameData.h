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
#ifndef __BLENDER_GAMEDATA__H__
#define __BLENDER_GAMEDATA__H__


// -------------------------------------------------- //
#include "blender_Common.h"
#include "blender_GameDome.h"
#include "blender_GameFraming.h"
#include "blender_RecastData.h"

namespace Blender {


    // ---------------------------------------------- //
    class GameData
    {
    public:
        GameFraming framing;
        short playerflag;
        short xplay;
        short yplay;
        short freqplay;
        short depth;
        short attrib;
        short rt1;
        short rt2;
        short aasamples;
        short pad4[3];
        GameDome dome;
        short stereoflag;
        short stereomode;
        float eyeseparation;
        RecastData recastData;
        float gravity;
        float activityBoxRadius;
        int flag;
        short mode;
        short matmode;
        short occlusionRes;
        short physicsEngine;
        short exitkey;
        short vsync;
        short ticrate;
        short maxlogicstep;
        short physubstep;
        short maxphystep;
        short obstacleSimulation;
        short raster_storage;
        float levelHeight;
        float deactivationtime;
        float lineardeactthreshold;
        float angulardeactthreshold;
        short lodflag;
        short pad2;
        int scehysteresis;
        int pad5;
    };
}


#endif//__BLENDER_GAMEDATA__H__
