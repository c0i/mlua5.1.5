
/*
** grep "ORDER OP" if you change these enums
*/

typedef enum {
/*----------------------------------------------------------------------
name        args    description
------------------------------------------------------------------------*/
OP_EQ,/*    A B C   if ((RK(B) == RK(C)) ~= A) then pc++        */
OP_NEWTABLE,/*  A B C   R(A) := {} (size = B,C)             */
OP_MUL,/*   A B C   R(A) := RK(B) * RK(C)               */
OP_SETLIST,/*   A B C   R(A)[(C-1)*FPF+i] := R(A+i), 1 <= i <= B    */
OP_TAILCALL,/*  A B C   return R(A)(R(A+1), ... ,R(A+B-1))      */
OP_GETGLOBAL,/* A Bx    R(A) := Gbl[Kst(Bx)]                */
OP_SELF,/*  A B C   R(A+1) := R(B); R(A) := R(B)[RK(C)]     */
OP_LOADBOOL,/*  A B C   R(A) := (Bool)B; if (C) pc++            */
OP_FORPREP,/*   A sBx   R(A)-=R(A+2); pc+=sBx               */
OP_LOADK,/* A Bx    R(A) := Kst(Bx)                 */
OP_RETURN,/*    A B return R(A), ... ,R(A+B-2)  (see note)  */
OP_LT,/*    A B C   if ((RK(B) <  RK(C)) ~= A) then pc++        */
OP_GETUPVAL,/*  A B R(A) := UpValue[B]              */
OP_TESTSET,/*   A B C   if (R(B) <=> C) then R(A) := R(B) else pc++ */
OP_TEST,/*  A C if not (R(A) <=> C) then pc++           */
OP_UNM,/*   A B R(A) := -R(B)                   */
OP_TFORLOOP,/*  A C R(A+3), ... ,R(A+2+C) := R(A)(R(A+1), R(A+2)); if R(A+3) ~= nil then R(A+2)=R(A+3) else pc++   */
OP_SETUPVAL,/*  A B UpValue[B] := R(A)              */
OP_POW,/*   A B C   R(A) := RK(B) ^ RK(C)               */
OP_GETTABLE,/*  A B C   R(A) := R(B)[RK(C)]             */
OP_CLOSE,/* A   close all variables in the stack up to (>=) R(A)*/
OP_LOADNIL,/*   A B R(A) := ... := R(B) := nil          */
OP_MOVE,/*  A B R(A) := R(B)                    */
OP_SETTABLE,/*  A B C   R(A)[RK(B)] := RK(C)                */
OP_LEN,/*   A B R(A) := length of R(B)              */
OP_LE,/*    A B C   if ((RK(B) <= RK(C)) ~= A) then pc++        */
OP_SUB,/*   A B C   R(A) := RK(B) - RK(C)               */
OP_SETGLOBAL,/* A Bx    Gbl[Kst(Bx)] := R(A)                */
OP_NOT,/*   A B R(A) := not R(B)                */
OP_DIV,/*   A B C   R(A) := RK(B) / RK(C)               */
OP_FORLOOP,/*   A sBx   R(A)+=R(A+2); if R(A) <?= R(A+1) then { pc+=sBx; R(A+3)=R(A) }*/
OP_CLOSURE,/*   A Bx    R(A) := closure(KPROTO[Bx], R(A), ... ,R(A+n))  */
OP_MOD,/*   A B C   R(A) := RK(B) % RK(C)               */
OP_ADD,/* A B C   R(A) := RK(B) + RK(C)                 */
OP_CONCAT,/*    A B C   R(A) := R(B).. ... ..R(C)           */
OP_CALL,/*    A B C   R(A), ... ,R(A+C-2) := R(A)(R(A+1), ... ,R(A+B-1)) */
OP_JMP,/*   sBx pc+=sBx                 */
OP_VARARG/* A B R(A), R(A+1), ..., R(A+B-1) = vararg        */
} OpCode;
    