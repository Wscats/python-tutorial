/**
 * @param {number[]} nums
 * @param {number} target
 * @return {number[]}
 */
var twoSum = function (nums, target) {
    for (let a = 0; a < nums.length; a++) {
        console.log(a)
        for (let b = 0; b < a; b++) {
            console.log(b)
        }
    }
};
twoSum([2, 4, 6, 9], 15)

// [0,1]
// [0,2]
// [0,3]
// [1,2]
// [1,3]
// [2,3]