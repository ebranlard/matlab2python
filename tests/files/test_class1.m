classdef MyClass < handle;
% Documentation: 
properties
    % Public
    prop_pub;
end
properties(SetAccess = private, Hidden = true)
    prop_priv=-1;
end
methods
    function o=MyClass(varargin)
        o.pro_pub=1
    end
    function read(o,value)
        o.check_extension();
        o.prop_pub=value;
    end
end % methods
end % class
