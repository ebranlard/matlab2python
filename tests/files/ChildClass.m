classdef ChildClass < TestClass
properties
    child_value; 
end
methods
    function this = ChildClass(varargin)
        this@TestClass(varargin);
        this.child_value = "Child";
    end
    function value = parse(this, input)
        value = this.child_value + input;
    end
    function value = read(this, value)
        value = read@TestClass(this, @this.parse(value));
    end
end
end
