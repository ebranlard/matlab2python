classdef FileCl < handle;
%% Documentation
properties
    % Public
    bReadOnly = false ;
    filepath;
    filename;
end
properties(SetAccess = private, Hidden = true)
    fid ; 
    line_number;
    pos_previous_line;
    current_filename;
    bVerbose=false;
end
properties(Abstract = true, Hidden=true);
    typical_extension; % need to be initialized by sub class
end
% --------------------------------------------------------------------------------
methods
    function o=FileCl(varargin)
       %    First argument is a filename
        if nargin==0
            o.setFilepath('');
        elseif nargin>=1
            % First argument is filename
            o.setFilepath(varargin{1});
            %o.read();
        else
           % fine, it's up to our children to handle the remaining arguments
        end
    end

    % --------------------------------------------------------------------------------{
    function read(o,file_name)
        % After reading, the oect is set to readonly, and the filepath matches the one that has been read
        if nargin==2
            o.setFilepath(file_name);
        end
        % --- Check of extension
        o.check_extension();
        % --- Changing  "current_filename", useful for error reporting
        o.current_filename=o.filepath;
    end
end % methods

end % class
