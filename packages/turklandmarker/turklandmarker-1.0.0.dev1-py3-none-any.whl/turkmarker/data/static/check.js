//FILE AUTOMATICALLY GENERATED
//DO NOT MANUALLY EDIT
function check(obj) {
    acc = [];
    if ((obj.P8 && obj.P8[0]) < (obj.P7 && obj.P7[0])) acc.push("invalid: P8 is to the left of P7");
    if ((obj.P9 && obj.P9[0]) < (obj.P8 && obj.P8[0])) acc.push("invalid: P9 is to the left of P8");
    if ((obj.P10 && obj.P10[0]) < (obj.P9 && obj.P9[0])) acc.push("invalid: P10 is to the left of P9");
    if ((obj.P11 && obj.P11[0]) < (obj.P10 && obj.P10[0])) acc.push("invalid: P11 is to the left of P10");
    if ((obj.P18 && obj.P18[0]) < (obj.P19 && obj.P19[0])) acc.push("invalid: P18 is to the left of P19");
    if ((obj.P21 && obj.P21[0]) < (obj.P20 && obj.P20[0])) acc.push("invalid: P21 is to the left of P20");
    if ((obj.P24 && obj.P24[0]) < (obj.P23 && obj.P23[0])) acc.push("invalid: P24 is to the left of P23");
    if ((obj.P28 && obj.P28[0]) < (obj.P29 && obj.P29[0])) acc.push("invalid: P28 is to the left of P29");
    if ((obj.P37 && obj.P37[0]) < (obj.P38 && obj.P38[0])) acc.push("invalid: P37 is to the left of P38");
    if ((obj.P44 && obj.P44[0]) < (obj.P43 && obj.P43[0])) acc.push("invalid: P44 is to the left of P43");
    if ((obj.P49 && obj.P49[0]) < (obj.P50 && obj.P50[0])) acc.push("invalid: P49 is to the left of P50");
    if ((obj.P4 && obj.P4[1]) < (obj.P3 && obj.P3[1])) acc.push("invalid: P3 is below P4");
    if ((obj.P6 && obj.P6[1]) < (obj.P5 && obj.P5[1])) acc.push("invalid: P5 is below P6");
    if ((obj.P15 && obj.P15[1]) < (obj.P16 && obj.P16[1])) acc.push("invalid: P16 is below P15");
    if ((obj.P17 && obj.P17[1]) < (obj.P18 && obj.P18[1])) acc.push("invalid: P18 is below P17");
    if ((obj.P29 && obj.P29[1]) < (obj.P28 && obj.P28[1])) acc.push("invalid: P28 is below P29");
    if ((obj.P37 && obj.P37[1]) < (obj.P38 && obj.P38[1])) acc.push("invalid: P38 is below P37");
    if ((obj.P50 && obj.P50[1]) < (obj.P49 && obj.P49[1])) acc.push("invalid: P49 is below P50");
    return acc;
}