from __future__ import absolute_import
from __future__ import print_function
import veriloggen
import dataflow_regionadd_filter_enable

expected_verilog = """
module test;

  reg CLK;
  reg RST;
  reg [32-1:0] xdata;
  reg xvalid;
  wire xready;
  reg [1-1:0] resetdata;
  reg resetvalid;
  wire resetready;
  reg [1-1:0] enabledata;
  reg enablevalid;
  wire enableready;
  wire signed [32-1:0] zdata;
  wire zvalid;
  reg zready;
  wire [1-1:0] vdata;
  wire vvalid;
  reg vready;

  main
  uut
  (
    .CLK(CLK),
    .RST(RST),
    .xdata(xdata),
    .xvalid(xvalid),
    .xready(xready),
    .resetdata(resetdata),
    .resetvalid(resetvalid),
    .resetready(resetready),
    .enabledata(enabledata),
    .enablevalid(enablevalid),
    .enableready(enableready),
    .zdata(zdata),
    .zvalid(zvalid),
    .zready(zready),
    .vdata(vdata),
    .vvalid(vvalid),
    .vready(vready)
  );

  reg reset_done;

  initial begin
    $dumpfile("uut.vcd");
    $dumpvars(0, uut);
  end


  initial begin
    CLK = 0;
    forever begin
      #5 CLK = !CLK;
    end
  end


  initial begin
    RST = 0;
    reset_done = 0;
    xdata = 0;
    xvalid = 0;
    enabledata = 0;
    enablevalid = 0;
    resetdata = 0;
    resetvalid = 0;
    zready = 0;
    #100;
    RST = 1;
    #100;
    RST = 0;
    #1000;
    reset_done = 1;
    @(posedge CLK);
    #1;
    #10000;
    $finish;
  end

  reg [32-1:0] xfsm;
  localparam xfsm_init = 0;
  reg [32-1:0] _tmp_0;
  localparam xfsm_1 = 1;
  localparam xfsm_2 = 2;
  localparam xfsm_3 = 3;
  localparam xfsm_4 = 4;
  localparam xfsm_5 = 5;
  localparam xfsm_6 = 6;
  localparam xfsm_7 = 7;
  localparam xfsm_8 = 8;
  localparam xfsm_9 = 9;
  localparam xfsm_10 = 10;
  localparam xfsm_11 = 11;
  localparam xfsm_12 = 12;
  localparam xfsm_13 = 13;
  localparam xfsm_14 = 14;
  localparam xfsm_15 = 15;
  localparam xfsm_16 = 16;
  localparam xfsm_17 = 17;
  localparam xfsm_18 = 18;
  localparam xfsm_19 = 19;
  localparam xfsm_20 = 20;
  localparam xfsm_21 = 21;
  localparam xfsm_22 = 22;
  localparam xfsm_23 = 23;
  localparam xfsm_24 = 24;

  always @(posedge CLK) begin
    if(RST) begin
      xfsm <= xfsm_init;
      _tmp_0 <= 0;
    end else begin
      case(xfsm)
        xfsm_init: begin
          xvalid <= 0;
          if(reset_done) begin
            xfsm <= xfsm_1;
          end 
        end
        xfsm_1: begin
          xfsm <= xfsm_2;
        end
        xfsm_2: begin
          xfsm <= xfsm_3;
        end
        xfsm_3: begin
          xfsm <= xfsm_4;
        end
        xfsm_4: begin
          xfsm <= xfsm_5;
        end
        xfsm_5: begin
          xfsm <= xfsm_6;
        end
        xfsm_6: begin
          xfsm <= xfsm_7;
        end
        xfsm_7: begin
          xfsm <= xfsm_8;
        end
        xfsm_8: begin
          xfsm <= xfsm_9;
        end
        xfsm_9: begin
          xfsm <= xfsm_10;
        end
        xfsm_10: begin
          xfsm <= xfsm_11;
        end
        xfsm_11: begin
          xvalid <= 1;
          xfsm <= xfsm_12;
        end
        xfsm_12: begin
          if(xready) begin
            xdata <= xdata + 1;
          end 
          if(xready) begin
            _tmp_0 <= _tmp_0 + 1;
          end 
          if((_tmp_0 == 5) && xready) begin
            xvalid <= 0;
          end 
          if((_tmp_0 == 5) && xready) begin
            xfsm <= xfsm_13;
          end 
        end
        xfsm_13: begin
          xfsm <= xfsm_14;
        end
        xfsm_14: begin
          xfsm <= xfsm_15;
        end
        xfsm_15: begin
          xfsm <= xfsm_16;
        end
        xfsm_16: begin
          xfsm <= xfsm_17;
        end
        xfsm_17: begin
          xfsm <= xfsm_18;
        end
        xfsm_18: begin
          xfsm <= xfsm_19;
        end
        xfsm_19: begin
          xfsm <= xfsm_20;
        end
        xfsm_20: begin
          xfsm <= xfsm_21;
        end
        xfsm_21: begin
          xfsm <= xfsm_22;
        end
        xfsm_22: begin
          xfsm <= xfsm_23;
        end
        xfsm_23: begin
          xvalid <= 1;
          if(xready) begin
            xdata <= xdata + 1;
          end 
          if(xready) begin
            _tmp_0 <= _tmp_0 + 1;
          end 
          if((_tmp_0 == 100) && xready) begin
            xvalid <= 0;
          end 
          if((_tmp_0 == 100) && xready) begin
            xfsm <= xfsm_24;
          end 
        end
      endcase
    end
  end

  reg [32-1:0] zfsm;
  localparam zfsm_init = 0;
  localparam zfsm_1 = 1;
  localparam zfsm_2 = 2;
  localparam zfsm_3 = 3;
  localparam zfsm_4 = 4;
  localparam zfsm_5 = 5;
  localparam zfsm_6 = 6;
  localparam zfsm_7 = 7;
  localparam zfsm_8 = 8;

  always @(posedge CLK) begin
    if(RST) begin
      zfsm <= zfsm_init;
    end else begin
      case(zfsm)
        zfsm_init: begin
          zready <= 0;
          if(reset_done) begin
            zfsm <= zfsm_1;
          end 
        end
        zfsm_1: begin
          zfsm <= zfsm_2;
        end
        zfsm_2: begin
          if(zvalid) begin
            zready <= 1;
          end 
          if(zvalid) begin
            zfsm <= zfsm_3;
          end 
        end
        zfsm_3: begin
          zready <= 0;
          zfsm <= zfsm_4;
        end
        zfsm_4: begin
          zready <= 0;
          zfsm <= zfsm_5;
        end
        zfsm_5: begin
          zready <= 0;
          zfsm <= zfsm_6;
        end
        zfsm_6: begin
          zready <= 0;
          zfsm <= zfsm_7;
        end
        zfsm_7: begin
          zready <= 0;
          zfsm <= zfsm_8;
        end
        zfsm_8: begin
          zfsm <= zfsm_2;
        end
      endcase
    end
  end

  reg [32-1:0] vfsm;
  localparam vfsm_init = 0;
  localparam vfsm_1 = 1;
  localparam vfsm_2 = 2;
  localparam vfsm_3 = 3;
  localparam vfsm_4 = 4;
  localparam vfsm_5 = 5;
  localparam vfsm_6 = 6;
  localparam vfsm_7 = 7;
  localparam vfsm_8 = 8;

  always @(posedge CLK) begin
    if(RST) begin
      vfsm <= vfsm_init;
    end else begin
      case(vfsm)
        vfsm_init: begin
          vready <= 0;
          if(reset_done) begin
            vfsm <= vfsm_1;
          end 
        end
        vfsm_1: begin
          vfsm <= vfsm_2;
        end
        vfsm_2: begin
          if(vvalid) begin
            vready <= 1;
          end 
          if(vvalid) begin
            vfsm <= vfsm_3;
          end 
        end
        vfsm_3: begin
          vready <= 0;
          vfsm <= vfsm_4;
        end
        vfsm_4: begin
          vready <= 0;
          vfsm <= vfsm_5;
        end
        vfsm_5: begin
          vready <= 0;
          vfsm <= vfsm_6;
        end
        vfsm_6: begin
          vready <= 0;
          vfsm <= vfsm_7;
        end
        vfsm_7: begin
          vready <= 0;
          vfsm <= vfsm_8;
        end
        vfsm_8: begin
          vfsm <= vfsm_2;
        end
      endcase
    end
  end

  reg [32-1:0] enable;
  localparam enable_init = 0;
  reg [32-1:0] enable_count;
  localparam enable_1 = 1;
  localparam enable_2 = 2;

  always @(posedge CLK) begin
    if(RST) begin
      enable <= enable_init;
      enable_count <= 0;
    end else begin
      case(enable)
        enable_init: begin
          if(reset_done) begin
            enable <= enable_1;
          end 
        end
        enable_1: begin
          enablevalid <= 1;
          if(enablevalid && enableready) begin
            enable_count <= enable_count + 1;
          end 
          if(enablevalid && enableready && (enable_count == 2)) begin
            enabledata <= 1;
          end 
          if(enablevalid && enableready && (enable_count == 2)) begin
            enable <= enable_2;
          end 
        end
        enable_2: begin
          if(enablevalid && enableready) begin
            enabledata <= 0;
          end 
          enable_count <= 0;
          if(enablevalid && enableready) begin
            enable <= enable_1;
          end 
        end
      endcase
    end
  end

  reg [32-1:0] reset;
  localparam reset_init = 0;
  reg [32-1:0] reset_count;
  localparam reset_1 = 1;
  localparam reset_2 = 2;

  always @(posedge CLK) begin
    if(RST) begin
      reset <= reset_init;
      reset_count <= 0;
    end else begin
      case(reset)
        reset_init: begin
          if(reset_done) begin
            reset <= reset_1;
          end 
        end
        reset_1: begin
          resetvalid <= 1;
          if(resetvalid && resetready) begin
            reset_count <= reset_count + 1;
          end 
          if(resetvalid && resetready && (reset_count == 2)) begin
            resetdata <= 0;
          end 
          if(resetvalid && resetready && (reset_count == 2)) begin
            reset <= reset_2;
          end 
        end
        reset_2: begin
          if(resetvalid && resetready) begin
            resetdata <= 0;
          end 
          reset_count <= 0;
          if(resetvalid && resetready) begin
            reset <= reset_1;
          end 
        end
      endcase
    end
  end


  always @(posedge CLK) begin
    if(reset_done) begin
      if(xvalid && xready) begin
        $display("xdata=%d", xdata);
      end 
      if(zvalid && zready) begin
        $display("zdata=%d", zdata);
      end 
      if(vvalid && vready) begin
        $display("vdata=%d", vdata);
      end 
    end 
  end


endmodule



module main
(
  input CLK,
  input RST,
  input [32-1:0] xdata,
  input xvalid,
  output xready,
  input [1-1:0] resetdata,
  input resetvalid,
  output resetready,
  input [1-1:0] enabledata,
  input enablevalid,
  output enableready,
  output signed [32-1:0] zdata,
  output zvalid,
  input zready,
  output [1-1:0] vdata,
  output vvalid,
  input vready
);

  reg [32-1:0] _tmp_data_0;
  reg _tmp_valid_0;
  wire _tmp_ready_0;
  reg [1-1:0] _tmp_data_1;
  reg _tmp_valid_1;
  wire _tmp_ready_1;
  assign enableready = (_tmp_ready_0 || !_tmp_valid_0) && (enablevalid && resetvalid) && ((_tmp_ready_1 || !_tmp_valid_1) && enablevalid);
  reg [1-1:0] _tmp_data_2;
  reg _tmp_valid_2;
  wire _tmp_ready_2;
  assign resetready = (_tmp_ready_0 || !_tmp_valid_0) && (enablevalid && resetvalid) && ((_tmp_ready_2 || !_tmp_valid_2) && resetvalid);
  reg [32-1:0] _tmp_data_3;
  reg _tmp_valid_3;
  wire _tmp_ready_3;
  assign xready = (_tmp_ready_3 || !_tmp_valid_3) && xvalid;
  reg [1-1:0] _tmp_data_4;
  reg _tmp_valid_4;
  wire _tmp_ready_4;
  assign _tmp_ready_0 = (_tmp_ready_4 || !_tmp_valid_4) && _tmp_valid_0;
  reg [1-1:0] _tmp_data_5;
  reg _tmp_valid_5;
  wire _tmp_ready_5;
  assign _tmp_ready_1 = (_tmp_ready_5 || !_tmp_valid_5) && _tmp_valid_1;
  reg [1-1:0] _tmp_data_6;
  reg _tmp_valid_6;
  wire _tmp_ready_6;
  assign _tmp_ready_2 = (_tmp_ready_6 || !_tmp_valid_6) && _tmp_valid_2;
  reg [32-1:0] _tmp_data_7;
  reg _tmp_valid_7;
  wire _tmp_ready_7;
  assign _tmp_ready_3 = (_tmp_ready_7 || !_tmp_valid_7) && _tmp_valid_3;
  reg [1-1:0] _tmp_data_8;
  reg [1-1:0] _tmp_data_9;
  reg _tmp_valid_9;
  wire _tmp_ready_9;
  assign _tmp_ready_4 = (_tmp_ready_9 || !_tmp_valid_9) && (_tmp_valid_4 && _tmp_valid_5);
  reg [1-1:0] _tmp_data_10;
  reg _tmp_valid_10;
  wire _tmp_ready_10;
  assign _tmp_ready_6 = (_tmp_ready_10 || !_tmp_valid_10) && _tmp_valid_6;
  reg [32-1:0] _tmp_data_11;
  reg _tmp_valid_11;
  wire _tmp_ready_11;
  assign _tmp_ready_7 = (_tmp_ready_11 || !_tmp_valid_11) && _tmp_valid_7;
  reg [1-1:0] _tmp_data_12;
  reg _tmp_valid_12;
  wire _tmp_ready_12;
  assign _tmp_ready_5 = (_tmp_ready_9 || !_tmp_valid_9) && (_tmp_valid_4 && _tmp_valid_5) && ((_tmp_ready_12 || !_tmp_valid_12) && _tmp_valid_5);
  reg [1-1:0] _tmp_data_13;
  reg [1-1:0] _tmp_data_14;
  reg _tmp_valid_14;
  wire _tmp_ready_14;
  assign _tmp_ready_10 = (_tmp_ready_14 || !_tmp_valid_14) && (_tmp_valid_10 && _tmp_valid_9);
  reg [32-1:0] _tmp_data_15;
  reg _tmp_valid_15;
  wire _tmp_ready_15;
  assign _tmp_ready_11 = (_tmp_ready_15 || !_tmp_valid_15) && _tmp_valid_11;
  reg [1-1:0] _tmp_data_16;
  reg _tmp_valid_16;
  wire _tmp_ready_16;
  assign _tmp_ready_12 = (_tmp_ready_16 || !_tmp_valid_16) && _tmp_valid_12;
  reg [1-1:0] _tmp_data_17;
  reg _tmp_valid_17;
  wire _tmp_ready_17;
  assign _tmp_ready_9 = (_tmp_ready_14 || !_tmp_valid_14) && (_tmp_valid_10 && _tmp_valid_9) && ((_tmp_ready_17 || !_tmp_valid_17) && _tmp_valid_9);
  reg [32-1:0] _tmp_data_18;
  reg _tmp_valid_18;
  wire _tmp_ready_18;
  assign _tmp_ready_16 = (_tmp_ready_18 || !_tmp_valid_18) && (_tmp_valid_15 && _tmp_valid_16 && _tmp_valid_14);
  assign _tmp_ready_15 = (_tmp_ready_18 || !_tmp_valid_18) && (_tmp_valid_15 && _tmp_valid_16 && _tmp_valid_14);
  assign _tmp_ready_14 = (_tmp_ready_18 || !_tmp_valid_18) && (_tmp_valid_15 && _tmp_valid_16 && _tmp_valid_14);
  reg [1-1:0] _tmp_data_19;
  reg _tmp_valid_19;
  wire _tmp_ready_19;
  assign _tmp_ready_17 = (_tmp_ready_19 || !_tmp_valid_19) && _tmp_valid_17;
  reg signed [32-1:0] _tmp_data_20;
  reg _tmp_valid_20;
  wire _tmp_ready_20;
  assign _tmp_ready_18 = (_tmp_ready_20 || !_tmp_valid_20) && (_tmp_valid_19 && _tmp_valid_18);
  reg [1-1:0] _tmp_data_21;
  reg _tmp_valid_21;
  wire _tmp_ready_21;
  assign _tmp_ready_19 = (_tmp_ready_20 || !_tmp_valid_20) && (_tmp_valid_19 && _tmp_valid_18) && ((_tmp_ready_21 || !_tmp_valid_21) && _tmp_valid_19);
  assign zdata = _tmp_data_20;
  assign zvalid = _tmp_valid_20;
  assign _tmp_ready_20 = zready;
  assign vdata = _tmp_data_21;
  assign vvalid = _tmp_valid_21;
  assign _tmp_ready_21 = vready;

  always @(posedge CLK) begin
    if(RST) begin
      _tmp_data_0 <= 1'd0;
      _tmp_valid_0 <= 0;
      _tmp_data_1 <= 0;
      _tmp_valid_1 <= 0;
      _tmp_data_2 <= 0;
      _tmp_valid_2 <= 0;
      _tmp_data_3 <= 0;
      _tmp_valid_3 <= 0;
      _tmp_data_4 <= 0;
      _tmp_valid_4 <= 0;
      _tmp_data_5 <= 0;
      _tmp_valid_5 <= 0;
      _tmp_data_6 <= 0;
      _tmp_valid_6 <= 0;
      _tmp_data_7 <= 0;
      _tmp_valid_7 <= 0;
      _tmp_data_8 <= 0;
      _tmp_data_9 <= 0;
      _tmp_valid_9 <= 0;
      _tmp_data_10 <= 0;
      _tmp_valid_10 <= 0;
      _tmp_data_11 <= 0;
      _tmp_valid_11 <= 0;
      _tmp_data_12 <= 0;
      _tmp_valid_12 <= 0;
      _tmp_data_13 <= 0;
      _tmp_data_14 <= 0;
      _tmp_valid_14 <= 0;
      _tmp_data_15 <= 0;
      _tmp_valid_15 <= 0;
      _tmp_data_16 <= 0;
      _tmp_valid_16 <= 0;
      _tmp_data_17 <= 0;
      _tmp_valid_17 <= 0;
      _tmp_data_18 <= 1'd0;
      _tmp_valid_18 <= 0;
      _tmp_data_19 <= 0;
      _tmp_valid_19 <= 0;
      _tmp_data_20 <= 0;
      _tmp_valid_20 <= 0;
      _tmp_data_21 <= 0;
      _tmp_valid_21 <= 0;
    end else begin
      if((_tmp_ready_0 || !_tmp_valid_0) && (enableready && resetready) && (enablevalid && resetvalid) && enabledata) begin
        _tmp_data_0 <= (_tmp_data_0 >= 3)? 0 : _tmp_data_0 + 2'd1;
      end 
      if(_tmp_valid_0 && _tmp_ready_0) begin
        _tmp_valid_0 <= 0;
      end 
      if((_tmp_ready_0 || !_tmp_valid_0) && (enableready && resetready)) begin
        _tmp_valid_0 <= enablevalid && resetvalid;
      end 
      if((_tmp_ready_0 || !_tmp_valid_0) && (enableready && resetready) && (enablevalid && resetvalid) && resetdata) begin
        _tmp_data_0 <= 1'd0;
      end 
      if((_tmp_ready_0 || !_tmp_valid_0) && (enableready && resetready) && (enablevalid && resetvalid) && enabledata && resetdata) begin
        _tmp_data_0 <= (1'd0 >= 3)? 0 : 1'd0 + 2'd1;
      end 
      if((_tmp_ready_1 || !_tmp_valid_1) && enableready && enablevalid) begin
        _tmp_data_1 <= enabledata;
      end 
      if(_tmp_valid_1 && _tmp_ready_1) begin
        _tmp_valid_1 <= 0;
      end 
      if((_tmp_ready_1 || !_tmp_valid_1) && enableready) begin
        _tmp_valid_1 <= enablevalid;
      end 
      if((_tmp_ready_2 || !_tmp_valid_2) && resetready && resetvalid) begin
        _tmp_data_2 <= resetdata;
      end 
      if(_tmp_valid_2 && _tmp_ready_2) begin
        _tmp_valid_2 <= 0;
      end 
      if((_tmp_ready_2 || !_tmp_valid_2) && resetready) begin
        _tmp_valid_2 <= resetvalid;
      end 
      if((_tmp_ready_3 || !_tmp_valid_3) && xready && xvalid) begin
        _tmp_data_3 <= xdata;
      end 
      if(_tmp_valid_3 && _tmp_ready_3) begin
        _tmp_valid_3 <= 0;
      end 
      if((_tmp_ready_3 || !_tmp_valid_3) && xready) begin
        _tmp_valid_3 <= xvalid;
      end 
      if((_tmp_ready_4 || !_tmp_valid_4) && _tmp_ready_0 && _tmp_valid_0) begin
        _tmp_data_4 <= _tmp_data_0 == 3'd3;
      end 
      if(_tmp_valid_4 && _tmp_ready_4) begin
        _tmp_valid_4 <= 0;
      end 
      if((_tmp_ready_4 || !_tmp_valid_4) && _tmp_ready_0) begin
        _tmp_valid_4 <= _tmp_valid_0;
      end 
      if((_tmp_ready_5 || !_tmp_valid_5) && _tmp_ready_1 && _tmp_valid_1) begin
        _tmp_data_5 <= _tmp_data_1;
      end 
      if(_tmp_valid_5 && _tmp_ready_5) begin
        _tmp_valid_5 <= 0;
      end 
      if((_tmp_ready_5 || !_tmp_valid_5) && _tmp_ready_1) begin
        _tmp_valid_5 <= _tmp_valid_1;
      end 
      if((_tmp_ready_6 || !_tmp_valid_6) && _tmp_ready_2 && _tmp_valid_2) begin
        _tmp_data_6 <= _tmp_data_2;
      end 
      if(_tmp_valid_6 && _tmp_ready_6) begin
        _tmp_valid_6 <= 0;
      end 
      if((_tmp_ready_6 || !_tmp_valid_6) && _tmp_ready_2) begin
        _tmp_valid_6 <= _tmp_valid_2;
      end 
      if((_tmp_ready_7 || !_tmp_valid_7) && _tmp_ready_3 && _tmp_valid_3) begin
        _tmp_data_7 <= _tmp_data_3;
      end 
      if(_tmp_valid_7 && _tmp_ready_7) begin
        _tmp_valid_7 <= 0;
      end 
      if((_tmp_ready_7 || !_tmp_valid_7) && _tmp_ready_3) begin
        _tmp_valid_7 <= _tmp_valid_3;
      end 
      if(_tmp_valid_4 && _tmp_ready_4) begin
        _tmp_data_8 <= _tmp_data_4;
      end 
      if((_tmp_ready_9 || !_tmp_valid_9) && (_tmp_ready_4 && _tmp_ready_5) && (_tmp_valid_4 && _tmp_valid_5)) begin
        _tmp_data_9 <= _tmp_data_8 && _tmp_data_5;
      end 
      if(_tmp_valid_9 && _tmp_ready_9) begin
        _tmp_valid_9 <= 0;
      end 
      if((_tmp_ready_9 || !_tmp_valid_9) && (_tmp_ready_4 && _tmp_ready_5)) begin
        _tmp_valid_9 <= _tmp_valid_4 && _tmp_valid_5;
      end 
      if((_tmp_ready_10 || !_tmp_valid_10) && _tmp_ready_6 && _tmp_valid_6) begin
        _tmp_data_10 <= _tmp_data_6;
      end 
      if(_tmp_valid_10 && _tmp_ready_10) begin
        _tmp_valid_10 <= 0;
      end 
      if((_tmp_ready_10 || !_tmp_valid_10) && _tmp_ready_6) begin
        _tmp_valid_10 <= _tmp_valid_6;
      end 
      if((_tmp_ready_11 || !_tmp_valid_11) && _tmp_ready_7 && _tmp_valid_7) begin
        _tmp_data_11 <= _tmp_data_7;
      end 
      if(_tmp_valid_11 && _tmp_ready_11) begin
        _tmp_valid_11 <= 0;
      end 
      if((_tmp_ready_11 || !_tmp_valid_11) && _tmp_ready_7) begin
        _tmp_valid_11 <= _tmp_valid_7;
      end 
      if((_tmp_ready_12 || !_tmp_valid_12) && _tmp_ready_5 && _tmp_valid_5) begin
        _tmp_data_12 <= _tmp_data_5;
      end 
      if(_tmp_valid_12 && _tmp_ready_12) begin
        _tmp_valid_12 <= 0;
      end 
      if((_tmp_ready_12 || !_tmp_valid_12) && _tmp_ready_5) begin
        _tmp_valid_12 <= _tmp_valid_5;
      end 
      if(_tmp_valid_9 && _tmp_ready_9) begin
        _tmp_data_13 <= _tmp_data_9;
      end 
      if((_tmp_ready_14 || !_tmp_valid_14) && (_tmp_ready_10 && _tmp_ready_9) && (_tmp_valid_10 && _tmp_valid_9)) begin
        _tmp_data_14 <= _tmp_data_10 || _tmp_data_13;
      end 
      if(_tmp_valid_14 && _tmp_ready_14) begin
        _tmp_valid_14 <= 0;
      end 
      if((_tmp_ready_14 || !_tmp_valid_14) && (_tmp_ready_10 && _tmp_ready_9)) begin
        _tmp_valid_14 <= _tmp_valid_10 && _tmp_valid_9;
      end 
      if((_tmp_ready_15 || !_tmp_valid_15) && _tmp_ready_11 && _tmp_valid_11) begin
        _tmp_data_15 <= _tmp_data_11;
      end 
      if(_tmp_valid_15 && _tmp_ready_15) begin
        _tmp_valid_15 <= 0;
      end 
      if((_tmp_ready_15 || !_tmp_valid_15) && _tmp_ready_11) begin
        _tmp_valid_15 <= _tmp_valid_11;
      end 
      if((_tmp_ready_16 || !_tmp_valid_16) && _tmp_ready_12 && _tmp_valid_12) begin
        _tmp_data_16 <= _tmp_data_12;
      end 
      if(_tmp_valid_16 && _tmp_ready_16) begin
        _tmp_valid_16 <= 0;
      end 
      if((_tmp_ready_16 || !_tmp_valid_16) && _tmp_ready_12) begin
        _tmp_valid_16 <= _tmp_valid_12;
      end 
      if((_tmp_ready_17 || !_tmp_valid_17) && _tmp_ready_9 && _tmp_valid_9) begin
        _tmp_data_17 <= _tmp_data_9;
      end 
      if(_tmp_valid_17 && _tmp_ready_17) begin
        _tmp_valid_17 <= 0;
      end 
      if((_tmp_ready_17 || !_tmp_valid_17) && _tmp_ready_9) begin
        _tmp_valid_17 <= _tmp_valid_9;
      end 
      if((_tmp_ready_18 || !_tmp_valid_18) && (_tmp_ready_15 && _tmp_ready_16 && _tmp_ready_14) && (_tmp_valid_15 && _tmp_valid_16 && _tmp_valid_14) && _tmp_data_16) begin
        _tmp_data_18 <= _tmp_data_18 + _tmp_data_15;
      end 
      if(_tmp_valid_18 && _tmp_ready_18) begin
        _tmp_valid_18 <= 0;
      end 
      if((_tmp_ready_18 || !_tmp_valid_18) && (_tmp_ready_15 && _tmp_ready_16 && _tmp_ready_14)) begin
        _tmp_valid_18 <= _tmp_valid_15 && _tmp_valid_16 && _tmp_valid_14;
      end 
      if((_tmp_ready_18 || !_tmp_valid_18) && (_tmp_ready_15 && _tmp_ready_16 && _tmp_ready_14) && (_tmp_valid_15 && _tmp_valid_16 && _tmp_valid_14) && _tmp_data_14) begin
        _tmp_data_18 <= 1'd0;
      end 
      if((_tmp_ready_18 || !_tmp_valid_18) && (_tmp_ready_15 && _tmp_ready_16 && _tmp_ready_14) && (_tmp_valid_15 && _tmp_valid_16 && _tmp_valid_14) && _tmp_data_16 && _tmp_data_14) begin
        _tmp_data_18 <= 1'd0 + _tmp_data_15;
      end 
      if((_tmp_ready_19 || !_tmp_valid_19) && _tmp_ready_17 && _tmp_valid_17) begin
        _tmp_data_19 <= _tmp_data_17;
      end 
      if(_tmp_valid_19 && _tmp_ready_19) begin
        _tmp_valid_19 <= 0;
      end 
      if((_tmp_ready_19 || !_tmp_valid_19) && _tmp_ready_17) begin
        _tmp_valid_19 <= _tmp_valid_17;
      end 
      if((_tmp_ready_20 || !_tmp_valid_20) && (_tmp_ready_19 && _tmp_ready_18) && (_tmp_valid_19 && _tmp_valid_18)) begin
        _tmp_data_20 <= (_tmp_data_19)? _tmp_data_18 : 1'd0;
      end 
      if(_tmp_valid_20 && _tmp_ready_20) begin
        _tmp_valid_20 <= 0;
      end 
      if((_tmp_ready_20 || !_tmp_valid_20) && (_tmp_ready_19 && _tmp_ready_18)) begin
        _tmp_valid_20 <= _tmp_valid_19 && _tmp_valid_18;
      end 
      if((_tmp_ready_21 || !_tmp_valid_21) && _tmp_ready_19 && _tmp_valid_19) begin
        _tmp_data_21 <= _tmp_data_19;
      end 
      if(_tmp_valid_21 && _tmp_ready_21) begin
        _tmp_valid_21 <= 0;
      end 
      if((_tmp_ready_21 || !_tmp_valid_21) && _tmp_ready_19) begin
        _tmp_valid_21 <= _tmp_valid_19;
      end 
    end
  end


endmodule
"""

def test():
    veriloggen.reset()
    test_module = dataflow_regionadd_filter_enable.mkTest()
    code = test_module.to_verilog()

    from pyverilog.vparser.parser import VerilogParser
    from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
    parser = VerilogParser()
    expected_ast = parser.parse(expected_verilog)
    codegen = ASTCodeGenerator()
    expected_code = codegen.visit(expected_ast)

    assert(expected_code == code)
