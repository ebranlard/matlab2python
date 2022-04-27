classdef ChildClass < MyClass
properties
    child_value; 
end
methods
    function this = ChildClass(varargin)
        this@MyClass(varargin);
    end
    function value = parse(this, input)
        value = this.child_value + input;
    end
    function read(o, value) 
        read@MyClass(o, @this.parse(value));
    end
end
end
