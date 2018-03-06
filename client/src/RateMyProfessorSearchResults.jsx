import React from 'react';
import {
  Form,
  Input,
  Row,
  Col,
  Button,
  Radio,
  Checkbox,
  AutoComplete,
  Rate,
  Modal,
  Pagination,
  Spin,
} from 'antd';
import 'antd/dist/antd.css';

const $ = require('jquery');

const FormItem = Form.Item;
const RadioButton = Radio.Button;
const RadioGroup = Radio.Group;
const CheckboxGroup = Checkbox.Group;
const Textarea = Input.TextArea;

const starNum = 5;

export default class RateMyProfessorSearchResults extends React.Component {
  constructor(props) {
    super(props);
    this.state = { loading: true };
    this.handlePageChange = this.handlePageChange.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ loading: true });
    if (nextProps.page.toString() in nextProps.results) {
      this.setState({ loading: false });
    }
  }

  handlePageChange(page) {
    this.setState({ loading: true });
    this.props.onPageChange(page);
  }

  render() {
    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 6 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 18 },
      },
    };

    return (
      <Modal
        title="搜索结果"
        style={{ top: 20 }}
        width={768}
        visible={this.props.visible}
        onCancel={this.props.onCancel}
        footer={
          <Pagination
            current={this.props.page}
            total={this.props.totalPages * 10}
            onChange={this.handlePageChange}
          />}
      >
        <Spin spinning={this.state.loading} delay={100}>
          <Form style={{ margin: 'auto', padding: 20, maxWidth: '100%' }}>
            <FormItem
              {...formItemLayout}
              label="课程名称"
            >
              <Input
                value={this.props.page.toString() in this.props.results ? this.props.results[this.props.page.toString()].course_title : ''}
              />
            </FormItem>
            <FormItem
              {...formItemLayout}
              label="教授姓名"
            >
              <Input
                value={this.props.page.toString() in this.props.results ? this.props.results[this.props.page.toString()].professor_name : ''}
              />
            </FormItem>
            <FormItem
              {...formItemLayout}
              label="所在学期"
            >
              <Input
                value={this.props.page.toString() in this.props.results ? `${this.props.results[this.props.page.toString()].year} ${this.props.results[this.props.page.toString()].season[0].toUpperCase()}${this.props.results[this.props.page.toString()].season.slice(1)}` : ''} />
            </FormItem>
            <FormItem
              {...formItemLayout}
              label="学分数量"
            >
              <RadioGroup
                value={this.props.page.toString() in this.props.results ? this.props.results[this.props.page.toString()].credits.toString() : ''}>
                <Radio value="1">1</Radio>
                <Radio value="2">2</Radio>
                <Radio value="3">3</Radio>
                <Radio value="4">4</Radio>
                <Radio value="5">5</Radio>
              </RadioGroup>
            </FormItem>
            <FormItem
              {...formItemLayout}
              label="课程类型"
            >
              <CheckboxGroup
                value={this.props.page.toString() in this.props.results ? (() => {
                  const values = [];
                  if (this.props.results[this.props.page.toString()].isHU) {
                    values.push('HU');
                  }
                  if (this.props.results[this.props.page.toString()].isSS) {
                    values.push('SS');
                  }
                  if (this.props.results[this.props.page.toString()].isNS) {
                    values.push('NS');
                  }
                  if (this.props.results[this.props.page.toString()].isID) {
                    values.push('ID');
                  }
                  if (this.props.results[this.props.page.toString()].isRE) {
                    values.push('RE');
                  }
                  if (this.props.results[this.props.page.toString()].isOther) {
                    values.push('Other');
                  }
                  return values;
                })() : []}
              >
                <Checkbox value="HU">HU</Checkbox>
                <Checkbox value="SS">SS</Checkbox>
                <Checkbox value="NS">NS</Checkbox>
                <Checkbox value="ID">ID</Checkbox>
                <Checkbox value="RE">RE</Checkbox>
                <Checkbox value="Other">Other</Checkbox>
              </CheckboxGroup>
            </FormItem>
            <FormItem
              {...formItemLayout}
              label="所得成绩"
            >
              <RadioGroup
                value={this.props.page.toString() in this.props.results ? this.props.results[this.props.page.toString()].grade : ''}
              >
                <RadioButton value="A Range">A Range</RadioButton>
                <RadioButton value="B Range">B Range</RadioButton>
                <RadioButton value="C Range">C Range</RadioButton>
                <RadioButton value="P/F">P/F</RadioButton>
                <RadioButton value="Others">Others</RadioButton>
              </RadioGroup>
            </FormItem>
            <FormItem {...formItemLayout} label="课程难度">
              <Rate
                value={this.props.page.toString() in this.props.results ? this.props.results[this.props.page.toString()].difficulty * starNum : 0}
                disabled
              />
            </FormItem>
            <FormItem {...formItemLayout} label="教授质量">
              <Rate
                value={this.props.page.toString() in this.props.results ? this.props.results[this.props.page.toString()].quality * starNum : 0}
                disabled
              />
            </FormItem>
            <FormItem {...formItemLayout} label="Workload">
              <Rate
                value={this.props.page.toString() in this.props.results ? this.props.results[this.props.page.toString()].workload * starNum : 0}
                disabled
              />
            </FormItem>
            <FormItem {...formItemLayout} label="推荐指数">
              <Rate
                value={this.props.page.toString() in this.props.results ? this.props.results[this.props.page.toString()].recommend * starNum : 0}
                disabled
              />
            </FormItem>
            <FormItem
              {...formItemLayout}
              label="相关建议"
            >
              <Textarea
                rows={3}
                style={{ resize: 'none' }}
                value={this.props.page.toString() in this.props.results ? this.props.results[this.props.page.toString()].suggestion : ''}
              />
            </FormItem>
          </Form>
        </Spin>
      </Modal>
    )
      ;
  }
}