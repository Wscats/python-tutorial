//时优 运用空间而减少了时间的使用
function swap(a, b) {
	var c;
	c = a;
	a = b;
	b = a;
}
//空优 运用时间而减少了空间的使用
function swap(a, b) {
	a = a + b;
	b = a - b;
	a = a - b;
}

function unique(arr) {
	var obj = {}
	var result = []
	for(var i in arr) {
		if(!obj[arr[i]]) {
			obj[arr[i]] = true;
			result.push(arr[i]);
		}
	}
	return result;
}

var i, sum = 0,
	n = 100; //执行1次
for(i = 1; i <= n; i++) { //执行 n+1次 
	sum = sum + i; //执行n次 
}
console.log(sum); //执行1次 

var number = 1;
while(number < n) {
	number = number * 2;
	//时间复杂度为O(1)的算法
	...
}

for(var i = 0; i < n; i++) {
	//时间复杂度为O(1)的算法
	...
}

for(var i = 0; i < n; i++) { //执行 n+1次 
	for(var j = 0; j < n; i++) { //执行 n+1次 
		//复杂度为O(1)的算法
		...
		//执行 n次 
	}
}

(2 n + 1)(n + 1) = 2 n ^ 2 + 3 n + 1