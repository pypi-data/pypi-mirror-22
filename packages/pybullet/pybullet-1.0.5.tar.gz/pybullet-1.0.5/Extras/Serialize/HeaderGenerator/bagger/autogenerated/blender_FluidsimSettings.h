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
#ifndef __BLENDER_FLUIDSIMSETTINGS__H__
#define __BLENDER_FLUIDSIMSETTINGS__H__


// -------------------------------------------------- //
#include "blender_Common.h"

namespace Blender {


    // ---------------------------------------------- //
    class FluidsimSettings
    {
    public:
        FluidsimModifierData *fmd;
        int threads;
        int pad1;
        short type;
        short show_advancedoptions;
        short resolutionxyz;
        short previewresxyz;
        float realsize;
        short guiDisplayMode;
        short renderDisplayMode;
        float viscosityValue;
        short viscosityMode;
        short viscosityExponent;
        vec3f grav;
        float animStart;
        float animEnd;
        int bakeStart;
        int bakeEnd;
        int frameOffset;
        int pad2;
        float gstar;
        int maxRefine;
        float iniVelx;
        float iniVely;
        float iniVelz;
        Mesh *orgMesh;
        Mesh *meshBB;
        char surfdataPath[1024];
        vec3f bbStart;
        vec3f bbSize;
        Ipo *ipo;
        short typeFlags;
        char domainNovecgen;
        char volumeInitType;
        float partSlipValue;
        int generateTracers;
        float generateParticles;
        float surfaceSmoothing;
        int surfaceSubdivs;
        int flag;
        float particleInfSize;
        float particleInfAlpha;
        float farFieldSize;
        FluidVertexVelocity *meshVelocities;
        int totvert;
        float cpsTimeStart;
        float cpsTimeEnd;
        float cpsQuality;
        float attractforceStrength;
        float attractforceRadius;
        float velocityforceStrength;
        float velocityforceRadius;
        int lastgoodframe;
        float animRate;
    };
}


#endif//__BLENDER_FLUIDSIMSETTINGS__H__
