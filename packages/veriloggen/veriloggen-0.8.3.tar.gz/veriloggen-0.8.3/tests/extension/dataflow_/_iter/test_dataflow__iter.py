from __future__ import absolute_import
from __future__ import print_function
import veriloggen
import dataflow__iter

expected_verilog = """
module test;

  reg CLK;
  reg RST;
  reg [4-1:0] xdata;
  reg [4-1:0] ydata;
  wire [4-1:0] zdata;
  reg xvalid;
  wire xready;
  assign xready = 1;
  reg yvalid;
  wire yready;
  assign yready = 1;
  wire zvalid;
  reg zready;
  assign zvalid = 1;

  main
  uut
  (
    .CLK(CLK),
    .RST(RST),
    .xdata(xdata),
    .ydata(ydata),
    .zdata(zdata)
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
    ydata = 0;
    yvalid = 0;
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
          xvalid <= 1;
          xfsm <= xfsm_2;
        end
        xfsm_2: begin
          if(xready) begin
            xdata <= xdata + 1;
          end 
          if(xready) begin
            _tmp_0 <= _tmp_0 + 1;
          end 
          if((_tmp_0 == 5) && xready) begin
            xfsm <= xfsm_3;
          end 
        end
        xfsm_3: begin
          if(xready) begin
            xdata <= xdata + 1;
          end 
          if(xready) begin
            _tmp_0 <= _tmp_0 + 1;
          end 
          if((_tmp_0 == 10) && xready) begin
            xfsm <= xfsm_4;
          end 
        end
      endcase
    end
  end

  reg [32-1:0] yfsm;
  localparam yfsm_init = 0;
  reg [32-1:0] _tmp_1;
  localparam yfsm_1 = 1;
  localparam yfsm_2 = 2;
  localparam yfsm_3 = 3;
  localparam yfsm_4 = 4;

  always @(posedge CLK) begin
    if(RST) begin
      yfsm <= yfsm_init;
      _tmp_1 <= 0;
    end else begin
      case(yfsm)
        yfsm_init: begin
          yvalid <= 0;
          if(reset_done) begin
            yfsm <= yfsm_1;
          end 
        end
        yfsm_1: begin
          yvalid <= 1;
          yfsm <= yfsm_2;
        end
        yfsm_2: begin
          if(yready) begin
            ydata <= ydata + 2;
          end 
          if(yready) begin
            _tmp_1 <= _tmp_1 + 1;
          end 
          if((_tmp_1 == 5) && yready) begin
            yfsm <= yfsm_3;
          end 
        end
        yfsm_3: begin
          if(yready) begin
            ydata <= ydata + 2;
          end 
          if(yready) begin
            _tmp_1 <= _tmp_1 + 1;
          end 
          if((_tmp_1 == 10) && yready) begin
            yfsm <= yfsm_4;
          end 
        end
      endcase
    end
  end

  reg [32-1:0] zfsm;
  localparam zfsm_init = 0;
  localparam zfsm_1 = 1;
  localparam zfsm_2 = 2;

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
        end
      endcase
    end
  end


  always @(posedge CLK) begin
    if(reset_done) begin
      $display("xdata=%d", xdata);
      $display("ydata=%d", ydata);
      $display("zdata=%d", zdata);
    end 
  end


endmodule



module main
(
  input CLK,
  input RST,
  input [4-1:0] xdata,
  input [4-1:0] ydata,
  output [4-1:0] zdata
);

  reg [1-1:0] _tmp_data_0;
  reg _tmp_valid_0;
  wire _tmp_ready_0;
  reg [1-1:0] _tmp_data_1;
  reg _tmp_valid_1;
  wire _tmp_ready_1;
  reg [1-1:0] _tmp_data_2;
  reg _tmp_valid_2;
  wire _tmp_ready_2;
  reg [1-1:0] _tmp_data_3;
  reg _tmp_valid_3;
  wire _tmp_ready_3;
  reg [1-1:0] _tmp_data_4;
  reg _tmp_valid_4;
  wire _tmp_ready_4;
  reg [1-1:0] _tmp_data_5;
  reg _tmp_valid_5;
  wire _tmp_ready_5;
  reg [1-1:0] _tmp_data_6;
  reg _tmp_valid_6;
  wire _tmp_ready_6;
  reg [1-1:0] _tmp_data_7;
  reg _tmp_valid_7;
  wire _tmp_ready_7;
  reg [1-1:0] _tmp_data_8;
  reg _tmp_valid_8;
  wire _tmp_ready_8;
  assign _tmp_ready_0 = (_tmp_ready_8 || !_tmp_valid_8) && (_tmp_valid_0 && _tmp_valid_1);
  assign _tmp_ready_1 = (_tmp_ready_8 || !_tmp_valid_8) && (_tmp_valid_0 && _tmp_valid_1);
  reg [1-1:0] _tmp_data_9;
  reg _tmp_valid_9;
  wire _tmp_ready_9;
  assign _tmp_ready_2 = (_tmp_ready_9 || !_tmp_valid_9) && _tmp_valid_2;
  reg [1-1:0] _tmp_data_10;
  reg _tmp_valid_10;
  wire _tmp_ready_10;
  assign _tmp_ready_3 = (_tmp_ready_10 || !_tmp_valid_10) && _tmp_valid_3;
  reg [1-1:0] _tmp_data_11;
  reg _tmp_valid_11;
  wire _tmp_ready_11;
  assign _tmp_ready_4 = (_tmp_ready_11 || !_tmp_valid_11) && _tmp_valid_4;
  reg [1-1:0] _tmp_data_12;
  reg _tmp_valid_12;
  wire _tmp_ready_12;
  assign _tmp_ready_5 = (_tmp_ready_12 || !_tmp_valid_12) && _tmp_valid_5;
  reg [1-1:0] _tmp_data_13;
  reg _tmp_valid_13;
  wire _tmp_ready_13;
  assign _tmp_ready_6 = (_tmp_ready_13 || !_tmp_valid_13) && _tmp_valid_6;
  reg [1-1:0] _tmp_data_14;
  reg _tmp_valid_14;
  wire _tmp_ready_14;
  assign _tmp_ready_7 = (_tmp_ready_14 || !_tmp_valid_14) && _tmp_valid_7;
  reg [1-1:0] _tmp_data_15;
  reg _tmp_valid_15;
  wire _tmp_ready_15;
  assign _tmp_ready_9 = (_tmp_ready_15 || !_tmp_valid_15) && (_tmp_valid_8 && _tmp_valid_9);
  reg [1-1:0] _tmp_data_16;
  reg _tmp_valid_16;
  wire _tmp_ready_16;
  assign _tmp_ready_10 = (_tmp_ready_16 || !_tmp_valid_16) && _tmp_valid_10;
  reg [1-1:0] _tmp_data_17;
  reg _tmp_valid_17;
  wire _tmp_ready_17;
  assign _tmp_ready_11 = (_tmp_ready_17 || !_tmp_valid_17) && _tmp_valid_11;
  reg [1-1:0] _tmp_data_18;
  reg _tmp_valid_18;
  wire _tmp_ready_18;
  assign _tmp_ready_12 = (_tmp_ready_18 || !_tmp_valid_18) && _tmp_valid_12;
  reg [1-1:0] _tmp_data_19;
  reg _tmp_valid_19;
  wire _tmp_ready_19;
  assign _tmp_ready_13 = (_tmp_ready_19 || !_tmp_valid_19) && _tmp_valid_13;
  reg [1-1:0] _tmp_data_20;
  reg _tmp_valid_20;
  wire _tmp_ready_20;
  assign _tmp_ready_14 = (_tmp_ready_20 || !_tmp_valid_20) && _tmp_valid_14;
  reg [1-1:0] _tmp_data_21;
  reg _tmp_valid_21;
  wire _tmp_ready_21;
  assign _tmp_ready_8 = (_tmp_ready_15 || !_tmp_valid_15) && (_tmp_valid_8 && _tmp_valid_9) && ((_tmp_ready_21 || !_tmp_valid_21) && _tmp_valid_8);
  reg [1-1:0] _tmp_data_22;
  reg _tmp_valid_22;
  wire _tmp_ready_22;
  assign _tmp_ready_15 = (_tmp_ready_22 || !_tmp_valid_22) && (_tmp_valid_15 && _tmp_valid_16);
  assign _tmp_ready_16 = (_tmp_ready_22 || !_tmp_valid_22) && (_tmp_valid_15 && _tmp_valid_16);
  reg [1-1:0] _tmp_data_23;
  reg _tmp_valid_23;
  wire _tmp_ready_23;
  assign _tmp_ready_17 = (_tmp_ready_23 || !_tmp_valid_23) && _tmp_valid_17;
  reg [1-1:0] _tmp_data_24;
  reg _tmp_valid_24;
  wire _tmp_ready_24;
  assign _tmp_ready_18 = (_tmp_ready_24 || !_tmp_valid_24) && _tmp_valid_18;
  reg [1-1:0] _tmp_data_25;
  reg _tmp_valid_25;
  wire _tmp_ready_25;
  assign _tmp_ready_19 = (_tmp_ready_25 || !_tmp_valid_25) && _tmp_valid_19;
  reg [1-1:0] _tmp_data_26;
  reg _tmp_valid_26;
  wire _tmp_ready_26;
  assign _tmp_ready_20 = (_tmp_ready_26 || !_tmp_valid_26) && _tmp_valid_20;
  reg [1-1:0] _tmp_data_27;
  reg _tmp_valid_27;
  wire _tmp_ready_27;
  assign _tmp_ready_21 = (_tmp_ready_27 || !_tmp_valid_27) && _tmp_valid_21;
  reg [1-1:0] _tmp_data_28;
  reg _tmp_valid_28;
  wire _tmp_ready_28;
  assign _tmp_ready_23 = (_tmp_ready_28 || !_tmp_valid_28) && (_tmp_valid_22 && _tmp_valid_23);
  reg [1-1:0] _tmp_data_29;
  reg _tmp_valid_29;
  wire _tmp_ready_29;
  assign _tmp_ready_24 = (_tmp_ready_29 || !_tmp_valid_29) && _tmp_valid_24;
  reg [1-1:0] _tmp_data_30;
  reg _tmp_valid_30;
  wire _tmp_ready_30;
  assign _tmp_ready_25 = (_tmp_ready_30 || !_tmp_valid_30) && _tmp_valid_25;
  reg [1-1:0] _tmp_data_31;
  reg _tmp_valid_31;
  wire _tmp_ready_31;
  assign _tmp_ready_26 = (_tmp_ready_31 || !_tmp_valid_31) && _tmp_valid_26;
  reg [1-1:0] _tmp_data_32;
  reg _tmp_valid_32;
  wire _tmp_ready_32;
  assign _tmp_ready_22 = (_tmp_ready_28 || !_tmp_valid_28) && (_tmp_valid_22 && _tmp_valid_23) && ((_tmp_ready_32 || !_tmp_valid_32) && _tmp_valid_22);
  reg [1-1:0] _tmp_data_33;
  reg _tmp_valid_33;
  wire _tmp_ready_33;
  assign _tmp_ready_27 = (_tmp_ready_33 || !_tmp_valid_33) && _tmp_valid_27;
  reg [1-1:0] _tmp_data_34;
  reg _tmp_valid_34;
  wire _tmp_ready_34;
  assign _tmp_ready_28 = (_tmp_ready_34 || !_tmp_valid_34) && (_tmp_valid_28 && _tmp_valid_29);
  assign _tmp_ready_29 = (_tmp_ready_34 || !_tmp_valid_34) && (_tmp_valid_28 && _tmp_valid_29);
  reg [1-1:0] _tmp_data_35;
  reg _tmp_valid_35;
  wire _tmp_ready_35;
  assign _tmp_ready_30 = (_tmp_ready_35 || !_tmp_valid_35) && _tmp_valid_30;
  reg [1-1:0] _tmp_data_36;
  reg _tmp_valid_36;
  wire _tmp_ready_36;
  assign _tmp_ready_31 = (_tmp_ready_36 || !_tmp_valid_36) && _tmp_valid_31;
  reg [1-1:0] _tmp_data_37;
  reg _tmp_valid_37;
  wire _tmp_ready_37;
  assign _tmp_ready_32 = (_tmp_ready_37 || !_tmp_valid_37) && _tmp_valid_32;
  reg [1-1:0] _tmp_data_38;
  reg _tmp_valid_38;
  wire _tmp_ready_38;
  assign _tmp_ready_33 = (_tmp_ready_38 || !_tmp_valid_38) && _tmp_valid_33;
  reg [1-1:0] _tmp_data_39;
  reg _tmp_valid_39;
  wire _tmp_ready_39;
  assign _tmp_ready_35 = (_tmp_ready_39 || !_tmp_valid_39) && (_tmp_valid_34 && _tmp_valid_35);
  reg [1-1:0] _tmp_data_40;
  reg _tmp_valid_40;
  wire _tmp_ready_40;
  assign _tmp_ready_36 = (_tmp_ready_40 || !_tmp_valid_40) && _tmp_valid_36;
  reg [1-1:0] _tmp_data_41;
  reg _tmp_valid_41;
  wire _tmp_ready_41;
  assign _tmp_ready_34 = (_tmp_ready_39 || !_tmp_valid_39) && (_tmp_valid_34 && _tmp_valid_35) && ((_tmp_ready_41 || !_tmp_valid_41) && _tmp_valid_34);
  reg [1-1:0] _tmp_data_42;
  reg _tmp_valid_42;
  wire _tmp_ready_42;
  assign _tmp_ready_37 = (_tmp_ready_42 || !_tmp_valid_42) && _tmp_valid_37;
  reg [1-1:0] _tmp_data_43;
  reg _tmp_valid_43;
  wire _tmp_ready_43;
  assign _tmp_ready_38 = (_tmp_ready_43 || !_tmp_valid_43) && _tmp_valid_38;
  reg [1-1:0] _tmp_data_44;
  reg _tmp_valid_44;
  wire _tmp_ready_44;
  assign _tmp_ready_39 = (_tmp_ready_44 || !_tmp_valid_44) && (_tmp_valid_39 && _tmp_valid_40);
  assign _tmp_ready_40 = (_tmp_ready_44 || !_tmp_valid_44) && (_tmp_valid_39 && _tmp_valid_40);
  reg [1-1:0] _tmp_data_45;
  reg _tmp_valid_45;
  wire _tmp_ready_45;
  assign _tmp_ready_41 = (_tmp_ready_45 || !_tmp_valid_45) && _tmp_valid_41;
  reg [1-1:0] _tmp_data_46;
  reg _tmp_valid_46;
  wire _tmp_ready_46;
  assign _tmp_ready_42 = (_tmp_ready_46 || !_tmp_valid_46) && _tmp_valid_42;
  reg [1-1:0] _tmp_data_47;
  reg _tmp_valid_47;
  wire _tmp_ready_47;
  assign _tmp_ready_43 = (_tmp_ready_47 || !_tmp_valid_47) && _tmp_valid_43;
  reg [4-1:0] _tmp_data_48;
  reg _tmp_valid_48;
  wire _tmp_ready_48;
  assign _tmp_ready_44 = (_tmp_ready_48 || !_tmp_valid_48) && (_tmp_valid_44 && _tmp_valid_45 && _tmp_valid_46 && _tmp_valid_47);
  assign _tmp_ready_45 = (_tmp_ready_48 || !_tmp_valid_48) && (_tmp_valid_44 && _tmp_valid_45 && _tmp_valid_46 && _tmp_valid_47);
  assign _tmp_ready_46 = (_tmp_ready_48 || !_tmp_valid_48) && (_tmp_valid_44 && _tmp_valid_45 && _tmp_valid_46 && _tmp_valid_47);
  assign _tmp_ready_47 = (_tmp_ready_48 || !_tmp_valid_48) && (_tmp_valid_44 && _tmp_valid_45 && _tmp_valid_46 && _tmp_valid_47);
  assign zdata = _tmp_data_48;
  assign _tmp_ready_48 = 1;

  always @(posedge CLK) begin
    if(RST) begin
      _tmp_data_0 <= 0;
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
      _tmp_valid_8 <= 0;
      _tmp_data_9 <= 0;
      _tmp_valid_9 <= 0;
      _tmp_data_10 <= 0;
      _tmp_valid_10 <= 0;
      _tmp_data_11 <= 0;
      _tmp_valid_11 <= 0;
      _tmp_data_12 <= 0;
      _tmp_valid_12 <= 0;
      _tmp_data_13 <= 0;
      _tmp_valid_13 <= 0;
      _tmp_data_14 <= 0;
      _tmp_valid_14 <= 0;
      _tmp_data_15 <= 0;
      _tmp_valid_15 <= 0;
      _tmp_data_16 <= 0;
      _tmp_valid_16 <= 0;
      _tmp_data_17 <= 0;
      _tmp_valid_17 <= 0;
      _tmp_data_18 <= 0;
      _tmp_valid_18 <= 0;
      _tmp_data_19 <= 0;
      _tmp_valid_19 <= 0;
      _tmp_data_20 <= 0;
      _tmp_valid_20 <= 0;
      _tmp_data_21 <= 0;
      _tmp_valid_21 <= 0;
      _tmp_data_22 <= 0;
      _tmp_valid_22 <= 0;
      _tmp_data_23 <= 0;
      _tmp_valid_23 <= 0;
      _tmp_data_24 <= 0;
      _tmp_valid_24 <= 0;
      _tmp_data_25 <= 0;
      _tmp_valid_25 <= 0;
      _tmp_data_26 <= 0;
      _tmp_valid_26 <= 0;
      _tmp_data_27 <= 0;
      _tmp_valid_27 <= 0;
      _tmp_data_28 <= 0;
      _tmp_valid_28 <= 0;
      _tmp_data_29 <= 0;
      _tmp_valid_29 <= 0;
      _tmp_data_30 <= 0;
      _tmp_valid_30 <= 0;
      _tmp_data_31 <= 0;
      _tmp_valid_31 <= 0;
      _tmp_data_32 <= 0;
      _tmp_valid_32 <= 0;
      _tmp_data_33 <= 0;
      _tmp_valid_33 <= 0;
      _tmp_data_34 <= 0;
      _tmp_valid_34 <= 0;
      _tmp_data_35 <= 0;
      _tmp_valid_35 <= 0;
      _tmp_data_36 <= 0;
      _tmp_valid_36 <= 0;
      _tmp_data_37 <= 0;
      _tmp_valid_37 <= 0;
      _tmp_data_38 <= 0;
      _tmp_valid_38 <= 0;
      _tmp_data_39 <= 0;
      _tmp_valid_39 <= 0;
      _tmp_data_40 <= 0;
      _tmp_valid_40 <= 0;
      _tmp_data_41 <= 0;
      _tmp_valid_41 <= 0;
      _tmp_data_42 <= 0;
      _tmp_valid_42 <= 0;
      _tmp_data_43 <= 0;
      _tmp_valid_43 <= 0;
      _tmp_data_44 <= 0;
      _tmp_valid_44 <= 0;
      _tmp_data_45 <= 0;
      _tmp_valid_45 <= 0;
      _tmp_data_46 <= 0;
      _tmp_valid_46 <= 0;
      _tmp_data_47 <= 0;
      _tmp_valid_47 <= 0;
      _tmp_data_48 <= 0;
      _tmp_valid_48 <= 0;
    end else begin
      if((_tmp_ready_0 || !_tmp_valid_0) && 1 && 1) begin
        _tmp_data_0 <= xdata[1'd0];
      end 
      if(_tmp_valid_0 && _tmp_ready_0) begin
        _tmp_valid_0 <= 0;
      end 
      if((_tmp_ready_0 || !_tmp_valid_0) && 1) begin
        _tmp_valid_0 <= 1;
      end 
      if((_tmp_ready_1 || !_tmp_valid_1) && 1 && 1) begin
        _tmp_data_1 <= ydata[1'd0];
      end 
      if(_tmp_valid_1 && _tmp_ready_1) begin
        _tmp_valid_1 <= 0;
      end 
      if((_tmp_ready_1 || !_tmp_valid_1) && 1) begin
        _tmp_valid_1 <= 1;
      end 
      if((_tmp_ready_2 || !_tmp_valid_2) && 1 && 1) begin
        _tmp_data_2 <= xdata[2'd1];
      end 
      if(_tmp_valid_2 && _tmp_ready_2) begin
        _tmp_valid_2 <= 0;
      end 
      if((_tmp_ready_2 || !_tmp_valid_2) && 1) begin
        _tmp_valid_2 <= 1;
      end 
      if((_tmp_ready_3 || !_tmp_valid_3) && 1 && 1) begin
        _tmp_data_3 <= ydata[2'd1];
      end 
      if(_tmp_valid_3 && _tmp_ready_3) begin
        _tmp_valid_3 <= 0;
      end 
      if((_tmp_ready_3 || !_tmp_valid_3) && 1) begin
        _tmp_valid_3 <= 1;
      end 
      if((_tmp_ready_4 || !_tmp_valid_4) && 1 && 1) begin
        _tmp_data_4 <= xdata[3'd2];
      end 
      if(_tmp_valid_4 && _tmp_ready_4) begin
        _tmp_valid_4 <= 0;
      end 
      if((_tmp_ready_4 || !_tmp_valid_4) && 1) begin
        _tmp_valid_4 <= 1;
      end 
      if((_tmp_ready_5 || !_tmp_valid_5) && 1 && 1) begin
        _tmp_data_5 <= ydata[3'd2];
      end 
      if(_tmp_valid_5 && _tmp_ready_5) begin
        _tmp_valid_5 <= 0;
      end 
      if((_tmp_ready_5 || !_tmp_valid_5) && 1) begin
        _tmp_valid_5 <= 1;
      end 
      if((_tmp_ready_6 || !_tmp_valid_6) && 1 && 1) begin
        _tmp_data_6 <= xdata[3'd3];
      end 
      if(_tmp_valid_6 && _tmp_ready_6) begin
        _tmp_valid_6 <= 0;
      end 
      if((_tmp_ready_6 || !_tmp_valid_6) && 1) begin
        _tmp_valid_6 <= 1;
      end 
      if((_tmp_ready_7 || !_tmp_valid_7) && 1 && 1) begin
        _tmp_data_7 <= ydata[3'd3];
      end 
      if(_tmp_valid_7 && _tmp_ready_7) begin
        _tmp_valid_7 <= 0;
      end 
      if((_tmp_ready_7 || !_tmp_valid_7) && 1) begin
        _tmp_valid_7 <= 1;
      end 
      if((_tmp_ready_8 || !_tmp_valid_8) && (_tmp_ready_0 && _tmp_ready_1) && (_tmp_valid_0 && _tmp_valid_1)) begin
        _tmp_data_8 <= _tmp_data_0 ^ _tmp_data_1;
      end 
      if(_tmp_valid_8 && _tmp_ready_8) begin
        _tmp_valid_8 <= 0;
      end 
      if((_tmp_ready_8 || !_tmp_valid_8) && (_tmp_ready_0 && _tmp_ready_1)) begin
        _tmp_valid_8 <= _tmp_valid_0 && _tmp_valid_1;
      end 
      if((_tmp_ready_9 || !_tmp_valid_9) && _tmp_ready_2 && _tmp_valid_2) begin
        _tmp_data_9 <= _tmp_data_2;
      end 
      if(_tmp_valid_9 && _tmp_ready_9) begin
        _tmp_valid_9 <= 0;
      end 
      if((_tmp_ready_9 || !_tmp_valid_9) && _tmp_ready_2) begin
        _tmp_valid_9 <= _tmp_valid_2;
      end 
      if((_tmp_ready_10 || !_tmp_valid_10) && _tmp_ready_3 && _tmp_valid_3) begin
        _tmp_data_10 <= _tmp_data_3;
      end 
      if(_tmp_valid_10 && _tmp_ready_10) begin
        _tmp_valid_10 <= 0;
      end 
      if((_tmp_ready_10 || !_tmp_valid_10) && _tmp_ready_3) begin
        _tmp_valid_10 <= _tmp_valid_3;
      end 
      if((_tmp_ready_11 || !_tmp_valid_11) && _tmp_ready_4 && _tmp_valid_4) begin
        _tmp_data_11 <= _tmp_data_4;
      end 
      if(_tmp_valid_11 && _tmp_ready_11) begin
        _tmp_valid_11 <= 0;
      end 
      if((_tmp_ready_11 || !_tmp_valid_11) && _tmp_ready_4) begin
        _tmp_valid_11 <= _tmp_valid_4;
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
      if((_tmp_ready_13 || !_tmp_valid_13) && _tmp_ready_6 && _tmp_valid_6) begin
        _tmp_data_13 <= _tmp_data_6;
      end 
      if(_tmp_valid_13 && _tmp_ready_13) begin
        _tmp_valid_13 <= 0;
      end 
      if((_tmp_ready_13 || !_tmp_valid_13) && _tmp_ready_6) begin
        _tmp_valid_13 <= _tmp_valid_6;
      end 
      if((_tmp_ready_14 || !_tmp_valid_14) && _tmp_ready_7 && _tmp_valid_7) begin
        _tmp_data_14 <= _tmp_data_7;
      end 
      if(_tmp_valid_14 && _tmp_ready_14) begin
        _tmp_valid_14 <= 0;
      end 
      if((_tmp_ready_14 || !_tmp_valid_14) && _tmp_ready_7) begin
        _tmp_valid_14 <= _tmp_valid_7;
      end 
      if((_tmp_ready_15 || !_tmp_valid_15) && (_tmp_ready_8 && _tmp_ready_9) && (_tmp_valid_8 && _tmp_valid_9)) begin
        _tmp_data_15 <= _tmp_data_8 ^ _tmp_data_9;
      end 
      if(_tmp_valid_15 && _tmp_ready_15) begin
        _tmp_valid_15 <= 0;
      end 
      if((_tmp_ready_15 || !_tmp_valid_15) && (_tmp_ready_8 && _tmp_ready_9)) begin
        _tmp_valid_15 <= _tmp_valid_8 && _tmp_valid_9;
      end 
      if((_tmp_ready_16 || !_tmp_valid_16) && _tmp_ready_10 && _tmp_valid_10) begin
        _tmp_data_16 <= _tmp_data_10;
      end 
      if(_tmp_valid_16 && _tmp_ready_16) begin
        _tmp_valid_16 <= 0;
      end 
      if((_tmp_ready_16 || !_tmp_valid_16) && _tmp_ready_10) begin
        _tmp_valid_16 <= _tmp_valid_10;
      end 
      if((_tmp_ready_17 || !_tmp_valid_17) && _tmp_ready_11 && _tmp_valid_11) begin
        _tmp_data_17 <= _tmp_data_11;
      end 
      if(_tmp_valid_17 && _tmp_ready_17) begin
        _tmp_valid_17 <= 0;
      end 
      if((_tmp_ready_17 || !_tmp_valid_17) && _tmp_ready_11) begin
        _tmp_valid_17 <= _tmp_valid_11;
      end 
      if((_tmp_ready_18 || !_tmp_valid_18) && _tmp_ready_12 && _tmp_valid_12) begin
        _tmp_data_18 <= _tmp_data_12;
      end 
      if(_tmp_valid_18 && _tmp_ready_18) begin
        _tmp_valid_18 <= 0;
      end 
      if((_tmp_ready_18 || !_tmp_valid_18) && _tmp_ready_12) begin
        _tmp_valid_18 <= _tmp_valid_12;
      end 
      if((_tmp_ready_19 || !_tmp_valid_19) && _tmp_ready_13 && _tmp_valid_13) begin
        _tmp_data_19 <= _tmp_data_13;
      end 
      if(_tmp_valid_19 && _tmp_ready_19) begin
        _tmp_valid_19 <= 0;
      end 
      if((_tmp_ready_19 || !_tmp_valid_19) && _tmp_ready_13) begin
        _tmp_valid_19 <= _tmp_valid_13;
      end 
      if((_tmp_ready_20 || !_tmp_valid_20) && _tmp_ready_14 && _tmp_valid_14) begin
        _tmp_data_20 <= _tmp_data_14;
      end 
      if(_tmp_valid_20 && _tmp_ready_20) begin
        _tmp_valid_20 <= 0;
      end 
      if((_tmp_ready_20 || !_tmp_valid_20) && _tmp_ready_14) begin
        _tmp_valid_20 <= _tmp_valid_14;
      end 
      if((_tmp_ready_21 || !_tmp_valid_21) && _tmp_ready_8 && _tmp_valid_8) begin
        _tmp_data_21 <= _tmp_data_8;
      end 
      if(_tmp_valid_21 && _tmp_ready_21) begin
        _tmp_valid_21 <= 0;
      end 
      if((_tmp_ready_21 || !_tmp_valid_21) && _tmp_ready_8) begin
        _tmp_valid_21 <= _tmp_valid_8;
      end 
      if((_tmp_ready_22 || !_tmp_valid_22) && (_tmp_ready_15 && _tmp_ready_16) && (_tmp_valid_15 && _tmp_valid_16)) begin
        _tmp_data_22 <= _tmp_data_15 ^ _tmp_data_16;
      end 
      if(_tmp_valid_22 && _tmp_ready_22) begin
        _tmp_valid_22 <= 0;
      end 
      if((_tmp_ready_22 || !_tmp_valid_22) && (_tmp_ready_15 && _tmp_ready_16)) begin
        _tmp_valid_22 <= _tmp_valid_15 && _tmp_valid_16;
      end 
      if((_tmp_ready_23 || !_tmp_valid_23) && _tmp_ready_17 && _tmp_valid_17) begin
        _tmp_data_23 <= _tmp_data_17;
      end 
      if(_tmp_valid_23 && _tmp_ready_23) begin
        _tmp_valid_23 <= 0;
      end 
      if((_tmp_ready_23 || !_tmp_valid_23) && _tmp_ready_17) begin
        _tmp_valid_23 <= _tmp_valid_17;
      end 
      if((_tmp_ready_24 || !_tmp_valid_24) && _tmp_ready_18 && _tmp_valid_18) begin
        _tmp_data_24 <= _tmp_data_18;
      end 
      if(_tmp_valid_24 && _tmp_ready_24) begin
        _tmp_valid_24 <= 0;
      end 
      if((_tmp_ready_24 || !_tmp_valid_24) && _tmp_ready_18) begin
        _tmp_valid_24 <= _tmp_valid_18;
      end 
      if((_tmp_ready_25 || !_tmp_valid_25) && _tmp_ready_19 && _tmp_valid_19) begin
        _tmp_data_25 <= _tmp_data_19;
      end 
      if(_tmp_valid_25 && _tmp_ready_25) begin
        _tmp_valid_25 <= 0;
      end 
      if((_tmp_ready_25 || !_tmp_valid_25) && _tmp_ready_19) begin
        _tmp_valid_25 <= _tmp_valid_19;
      end 
      if((_tmp_ready_26 || !_tmp_valid_26) && _tmp_ready_20 && _tmp_valid_20) begin
        _tmp_data_26 <= _tmp_data_20;
      end 
      if(_tmp_valid_26 && _tmp_ready_26) begin
        _tmp_valid_26 <= 0;
      end 
      if((_tmp_ready_26 || !_tmp_valid_26) && _tmp_ready_20) begin
        _tmp_valid_26 <= _tmp_valid_20;
      end 
      if((_tmp_ready_27 || !_tmp_valid_27) && _tmp_ready_21 && _tmp_valid_21) begin
        _tmp_data_27 <= _tmp_data_21;
      end 
      if(_tmp_valid_27 && _tmp_ready_27) begin
        _tmp_valid_27 <= 0;
      end 
      if((_tmp_ready_27 || !_tmp_valid_27) && _tmp_ready_21) begin
        _tmp_valid_27 <= _tmp_valid_21;
      end 
      if((_tmp_ready_28 || !_tmp_valid_28) && (_tmp_ready_22 && _tmp_ready_23) && (_tmp_valid_22 && _tmp_valid_23)) begin
        _tmp_data_28 <= _tmp_data_22 ^ _tmp_data_23;
      end 
      if(_tmp_valid_28 && _tmp_ready_28) begin
        _tmp_valid_28 <= 0;
      end 
      if((_tmp_ready_28 || !_tmp_valid_28) && (_tmp_ready_22 && _tmp_ready_23)) begin
        _tmp_valid_28 <= _tmp_valid_22 && _tmp_valid_23;
      end 
      if((_tmp_ready_29 || !_tmp_valid_29) && _tmp_ready_24 && _tmp_valid_24) begin
        _tmp_data_29 <= _tmp_data_24;
      end 
      if(_tmp_valid_29 && _tmp_ready_29) begin
        _tmp_valid_29 <= 0;
      end 
      if((_tmp_ready_29 || !_tmp_valid_29) && _tmp_ready_24) begin
        _tmp_valid_29 <= _tmp_valid_24;
      end 
      if((_tmp_ready_30 || !_tmp_valid_30) && _tmp_ready_25 && _tmp_valid_25) begin
        _tmp_data_30 <= _tmp_data_25;
      end 
      if(_tmp_valid_30 && _tmp_ready_30) begin
        _tmp_valid_30 <= 0;
      end 
      if((_tmp_ready_30 || !_tmp_valid_30) && _tmp_ready_25) begin
        _tmp_valid_30 <= _tmp_valid_25;
      end 
      if((_tmp_ready_31 || !_tmp_valid_31) && _tmp_ready_26 && _tmp_valid_26) begin
        _tmp_data_31 <= _tmp_data_26;
      end 
      if(_tmp_valid_31 && _tmp_ready_31) begin
        _tmp_valid_31 <= 0;
      end 
      if((_tmp_ready_31 || !_tmp_valid_31) && _tmp_ready_26) begin
        _tmp_valid_31 <= _tmp_valid_26;
      end 
      if((_tmp_ready_32 || !_tmp_valid_32) && _tmp_ready_22 && _tmp_valid_22) begin
        _tmp_data_32 <= _tmp_data_22;
      end 
      if(_tmp_valid_32 && _tmp_ready_32) begin
        _tmp_valid_32 <= 0;
      end 
      if((_tmp_ready_32 || !_tmp_valid_32) && _tmp_ready_22) begin
        _tmp_valid_32 <= _tmp_valid_22;
      end 
      if((_tmp_ready_33 || !_tmp_valid_33) && _tmp_ready_27 && _tmp_valid_27) begin
        _tmp_data_33 <= _tmp_data_27;
      end 
      if(_tmp_valid_33 && _tmp_ready_33) begin
        _tmp_valid_33 <= 0;
      end 
      if((_tmp_ready_33 || !_tmp_valid_33) && _tmp_ready_27) begin
        _tmp_valid_33 <= _tmp_valid_27;
      end 
      if((_tmp_ready_34 || !_tmp_valid_34) && (_tmp_ready_28 && _tmp_ready_29) && (_tmp_valid_28 && _tmp_valid_29)) begin
        _tmp_data_34 <= _tmp_data_28 ^ _tmp_data_29;
      end 
      if(_tmp_valid_34 && _tmp_ready_34) begin
        _tmp_valid_34 <= 0;
      end 
      if((_tmp_ready_34 || !_tmp_valid_34) && (_tmp_ready_28 && _tmp_ready_29)) begin
        _tmp_valid_34 <= _tmp_valid_28 && _tmp_valid_29;
      end 
      if((_tmp_ready_35 || !_tmp_valid_35) && _tmp_ready_30 && _tmp_valid_30) begin
        _tmp_data_35 <= _tmp_data_30;
      end 
      if(_tmp_valid_35 && _tmp_ready_35) begin
        _tmp_valid_35 <= 0;
      end 
      if((_tmp_ready_35 || !_tmp_valid_35) && _tmp_ready_30) begin
        _tmp_valid_35 <= _tmp_valid_30;
      end 
      if((_tmp_ready_36 || !_tmp_valid_36) && _tmp_ready_31 && _tmp_valid_31) begin
        _tmp_data_36 <= _tmp_data_31;
      end 
      if(_tmp_valid_36 && _tmp_ready_36) begin
        _tmp_valid_36 <= 0;
      end 
      if((_tmp_ready_36 || !_tmp_valid_36) && _tmp_ready_31) begin
        _tmp_valid_36 <= _tmp_valid_31;
      end 
      if((_tmp_ready_37 || !_tmp_valid_37) && _tmp_ready_32 && _tmp_valid_32) begin
        _tmp_data_37 <= _tmp_data_32;
      end 
      if(_tmp_valid_37 && _tmp_ready_37) begin
        _tmp_valid_37 <= 0;
      end 
      if((_tmp_ready_37 || !_tmp_valid_37) && _tmp_ready_32) begin
        _tmp_valid_37 <= _tmp_valid_32;
      end 
      if((_tmp_ready_38 || !_tmp_valid_38) && _tmp_ready_33 && _tmp_valid_33) begin
        _tmp_data_38 <= _tmp_data_33;
      end 
      if(_tmp_valid_38 && _tmp_ready_38) begin
        _tmp_valid_38 <= 0;
      end 
      if((_tmp_ready_38 || !_tmp_valid_38) && _tmp_ready_33) begin
        _tmp_valid_38 <= _tmp_valid_33;
      end 
      if((_tmp_ready_39 || !_tmp_valid_39) && (_tmp_ready_34 && _tmp_ready_35) && (_tmp_valid_34 && _tmp_valid_35)) begin
        _tmp_data_39 <= _tmp_data_34 ^ _tmp_data_35;
      end 
      if(_tmp_valid_39 && _tmp_ready_39) begin
        _tmp_valid_39 <= 0;
      end 
      if((_tmp_ready_39 || !_tmp_valid_39) && (_tmp_ready_34 && _tmp_ready_35)) begin
        _tmp_valid_39 <= _tmp_valid_34 && _tmp_valid_35;
      end 
      if((_tmp_ready_40 || !_tmp_valid_40) && _tmp_ready_36 && _tmp_valid_36) begin
        _tmp_data_40 <= _tmp_data_36;
      end 
      if(_tmp_valid_40 && _tmp_ready_40) begin
        _tmp_valid_40 <= 0;
      end 
      if((_tmp_ready_40 || !_tmp_valid_40) && _tmp_ready_36) begin
        _tmp_valid_40 <= _tmp_valid_36;
      end 
      if((_tmp_ready_41 || !_tmp_valid_41) && _tmp_ready_34 && _tmp_valid_34) begin
        _tmp_data_41 <= _tmp_data_34;
      end 
      if(_tmp_valid_41 && _tmp_ready_41) begin
        _tmp_valid_41 <= 0;
      end 
      if((_tmp_ready_41 || !_tmp_valid_41) && _tmp_ready_34) begin
        _tmp_valid_41 <= _tmp_valid_34;
      end 
      if((_tmp_ready_42 || !_tmp_valid_42) && _tmp_ready_37 && _tmp_valid_37) begin
        _tmp_data_42 <= _tmp_data_37;
      end 
      if(_tmp_valid_42 && _tmp_ready_42) begin
        _tmp_valid_42 <= 0;
      end 
      if((_tmp_ready_42 || !_tmp_valid_42) && _tmp_ready_37) begin
        _tmp_valid_42 <= _tmp_valid_37;
      end 
      if((_tmp_ready_43 || !_tmp_valid_43) && _tmp_ready_38 && _tmp_valid_38) begin
        _tmp_data_43 <= _tmp_data_38;
      end 
      if(_tmp_valid_43 && _tmp_ready_43) begin
        _tmp_valid_43 <= 0;
      end 
      if((_tmp_ready_43 || !_tmp_valid_43) && _tmp_ready_38) begin
        _tmp_valid_43 <= _tmp_valid_38;
      end 
      if((_tmp_ready_44 || !_tmp_valid_44) && (_tmp_ready_39 && _tmp_ready_40) && (_tmp_valid_39 && _tmp_valid_40)) begin
        _tmp_data_44 <= _tmp_data_39 ^ _tmp_data_40;
      end 
      if(_tmp_valid_44 && _tmp_ready_44) begin
        _tmp_valid_44 <= 0;
      end 
      if((_tmp_ready_44 || !_tmp_valid_44) && (_tmp_ready_39 && _tmp_ready_40)) begin
        _tmp_valid_44 <= _tmp_valid_39 && _tmp_valid_40;
      end 
      if((_tmp_ready_45 || !_tmp_valid_45) && _tmp_ready_41 && _tmp_valid_41) begin
        _tmp_data_45 <= _tmp_data_41;
      end 
      if(_tmp_valid_45 && _tmp_ready_45) begin
        _tmp_valid_45 <= 0;
      end 
      if((_tmp_ready_45 || !_tmp_valid_45) && _tmp_ready_41) begin
        _tmp_valid_45 <= _tmp_valid_41;
      end 
      if((_tmp_ready_46 || !_tmp_valid_46) && _tmp_ready_42 && _tmp_valid_42) begin
        _tmp_data_46 <= _tmp_data_42;
      end 
      if(_tmp_valid_46 && _tmp_ready_46) begin
        _tmp_valid_46 <= 0;
      end 
      if((_tmp_ready_46 || !_tmp_valid_46) && _tmp_ready_42) begin
        _tmp_valid_46 <= _tmp_valid_42;
      end 
      if((_tmp_ready_47 || !_tmp_valid_47) && _tmp_ready_43 && _tmp_valid_43) begin
        _tmp_data_47 <= _tmp_data_43;
      end 
      if(_tmp_valid_47 && _tmp_ready_47) begin
        _tmp_valid_47 <= 0;
      end 
      if((_tmp_ready_47 || !_tmp_valid_47) && _tmp_ready_43) begin
        _tmp_valid_47 <= _tmp_valid_43;
      end 
      if((_tmp_ready_48 || !_tmp_valid_48) && (_tmp_ready_44 && _tmp_ready_45 && _tmp_ready_46 && _tmp_ready_47) && (_tmp_valid_44 && _tmp_valid_45 && _tmp_valid_46 && _tmp_valid_47)) begin
        _tmp_data_48 <= { _tmp_data_44, _tmp_data_45, _tmp_data_46, _tmp_data_47 };
      end 
      if(_tmp_valid_48 && _tmp_ready_48) begin
        _tmp_valid_48 <= 0;
      end 
      if((_tmp_ready_48 || !_tmp_valid_48) && (_tmp_ready_44 && _tmp_ready_45 && _tmp_ready_46 && _tmp_ready_47)) begin
        _tmp_valid_48 <= _tmp_valid_44 && _tmp_valid_45 && _tmp_valid_46 && _tmp_valid_47;
      end 
    end
  end


endmodule
"""

def test():
    veriloggen.reset()
    test_module = dataflow__iter.mkTest()
    code = test_module.to_verilog()

    from pyverilog.vparser.parser import VerilogParser
    from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
    parser = VerilogParser()
    expected_ast = parser.parse(expected_verilog)
    codegen = ASTCodeGenerator()
    expected_code = codegen.visit(expected_ast)

    assert(expected_code == code)
