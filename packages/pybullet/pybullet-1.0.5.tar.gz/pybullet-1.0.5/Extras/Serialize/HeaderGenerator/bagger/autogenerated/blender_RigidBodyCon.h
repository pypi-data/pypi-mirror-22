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
#ifndef __BLENDER_RIGIDBODYCON__H__
#define __BLENDER_RIGIDBODYCON__H__


// -------------------------------------------------- //
#include "blender_Common.h"

namespace Blender {


    // ---------------------------------------------- //
    class RigidBodyCon
    {
    public:
        Object *ob1;
        Object *ob2;
        short type;
        short num_solver_iterations;
        int flag;
        float breaking_threshold;
        float pad;
        float limit_lin_x_lower;
        float limit_lin_x_upper;
        float limit_lin_y_lower;
        float limit_lin_y_upper;
        float limit_lin_z_lower;
        float limit_lin_z_upper;
        float limit_ang_x_lower;
        float limit_ang_x_upper;
        float limit_ang_y_lower;
        float limit_ang_y_upper;
        float limit_ang_z_lower;
        float limit_ang_z_upper;
        float spring_stiffness_x;
        float spring_stiffness_y;
        float spring_stiffness_z;
        float spring_damping_x;
        float spring_damping_y;
        float spring_damping_z;
        float motor_lin_target_velocity;
        float motor_ang_target_velocity;
        float motor_lin_max_impulse;
        float motor_ang_max_impulse;
        void *physics_constraint;
    };
}


#endif//__BLENDER_RIGIDBODYCON__H__
