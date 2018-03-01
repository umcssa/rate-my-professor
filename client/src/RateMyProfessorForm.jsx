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
} from 'antd';

const $ = require('jquery');

const FormItem = Form.Item;
const RadioButton = Radio.Button;
const RadioGroup = Radio.Group;
const CheckboxGroup = Checkbox.Group;
const Textarea = Input.TextArea;

const apiRootPath = 'http://54.201.89.84/api/rate-my-professor/';

class RateMyProfessorForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            confirmDirty: false,
            all_departments: [],
            all_courses: [],
            all_professors: [],
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.updateDepartment = this.updateDepartment.bind(this);
    }

    componentDidMount() {
        // fetch('examples/example.json')
        //     .then((response) => {
        //         if (!response.ok) {
        //             throw Error(response.statusText);
        //         }
        //         return response.json();
        //     })
        //     .then((responseAsJson) => {
        //         console.log(responseAsJson);
        //     })
        //     .catch((error) => {
        //         console.log('Looks like there was a problem: \n', error);
        //     });

        $.ajax({
            method: 'GET',
            url: `${apiRootPath}get-departments/`,
        }).done((msg) => {
            this.setState({ all_departments: JSON.parse(msg) });
        });
    }

    updateDepartment(department) {
        $.ajax({
            method: 'GET',
            url: `${apiRootPath}get-courses/?department=${department}`,
        }).done((msg) => {
            this.setState({ all_courses: JSON.parse(msg) });
        });
        $.ajax({
            method: 'GET',
            url: `${apiRootPath}get-professors/?department=${department}`,
        }).done((msg) => {
            this.setState({ all_professors: JSON.parse(msg) });
        });
    }

    handleSubmit(e) {
        e.preventDefault();
        const starNum = 5;
        this.props.form.validateFieldsAndScroll((err, values) => {
            if (!err) {
                const data = values;
                data.difficulty /= starNum;
                data.quality /= starNum;
                data.workload /= starNum;
                data.recommend /= starNum;
                $.ajax({
                    method: 'POST',
                    url: `${apiRootPath}rmp-form/`,
                    data,
                }).done((msg) => {
                    if (msg === 'success') {
                        Modal.success({
                            title: '您的评价已保存，感谢参与！',
                            okText: '前往搜索界面',
                            onOk() {
                                window.location.href = '/rate-my-professor/search/';
                            },
                        });
                    } else if (msg === 'invalid') {
                        Modal.warning({
                            title: '评价内容不符合要求，请修改后再提交！',
                        });
                    } else {
                        Modal.error({
                            title: '服务器忙，请稍后重新提交！',
                        });
                    }
                });
            }
        });
    }

    render() {
        const {getFieldDecorator} = this.props.form;

        const formItemLayout = {
            labelCol: {
                xs: {span: 24},
                sm: {span: 6},
            },
            wrapperCol: {
                xs: {span: 24},
                sm: {span: 18},
            },
        };
        const tailFormItemLayout = {
            wrapperCol: {
                xs: {
                    span: 24,
                    offset: 0,
                },
                sm: {
                    span: 16,
                    offset: 6,
                },
            },
        };

        return (
            <Form onSubmit={this.handleSubmit} style={{margin: 'auto', padding: 20, maxWidth: 1000}}>
                <FormItem
                    {...formItemLayout}
                    label="课程院系"
                >
                    {getFieldDecorator('department', {
                        rules: [{required: true, message: '请输入课程院系！'}],
                    })(
                        <AutoComplete
                            dataSource={this.state.all_departments}
                            onChange={this.updateDepartment}
                            filterOption={(inputValue, option) =>
                                option.props.children.toUpperCase().indexOf(inputValue.toUpperCase()) !== -1}
                        >
                            <Input/>
                        </AutoComplete>,
                    )}
                </FormItem>
                <FormItem
                    {...formItemLayout}
                    label="课程名称"
                >
                    {getFieldDecorator('course', {
                        rules: [{required: true, message: '请输入课程名称！'}],
                    })(
                        <AutoComplete
                            dataSource={this.state.all_courses}
                            filterOption={(inputValue, option) =>
                                option.props.children.toUpperCase().indexOf(inputValue.toUpperCase()) !== -1}
                        >
                            <Input/>
                        </AutoComplete>,
                    )}
                </FormItem>
                <FormItem
                    {...formItemLayout}
                    label="教授姓名"
                >
                    {getFieldDecorator('professor', {
                        rules: [{required: true, message: '请输入教授姓名！'}],
                    })(
                        <AutoComplete
                            dataSource={this.state.all_professors}
                            filterOption={(inputValue, option) =>
                                option.props.children.toUpperCase().indexOf(inputValue.toUpperCase()) !== -1}
                        >
                            <Input/>
                        </AutoComplete>,
                    )}
                </FormItem>
                <FormItem
                    {...formItemLayout}
                    label="所在学期"
                >
                    {getFieldDecorator('semester', {
                        rules: [{required: true, message: '请输入所在学期！', whitespace: true}],
                    })(
                        <Input placeholder="Eg: 2017 Winter"/>,
                    )}
                </FormItem>
                <FormItem
                    {...formItemLayout}
                    label="学分数量"
                >
                    {getFieldDecorator('credits', {
                        rules: [{required: true, message: '请选择学分数量！'}],
                    })(
                        <RadioGroup>
                            <Radio value="1">1</Radio>
                            <Radio value="2">2</Radio>
                            <Radio value="3">3</Radio>
                            <Radio value="4">4</Radio>
                            <Radio value="5">5</Radio>
                        </RadioGroup>,
                    )}
                </FormItem>
                <FormItem
                    {...formItemLayout}
                    label="课程类型"
                >
                    {getFieldDecorator('type', {
                        rules: [
                            {required: true, message: '请选择课程类型！', type: 'array'},
                        ],
                    })(
                        <CheckboxGroup>
                            <Checkbox value="HU">HU</Checkbox>
                            <Checkbox value="SS">SS</Checkbox>
                            <Checkbox value="NS">NS</Checkbox>
                            <Checkbox value="ID">ID</Checkbox>
                            <Checkbox value="RE">RE</Checkbox>
                            <Checkbox value="Other">Other</Checkbox>
                        </CheckboxGroup>,
                    )}
                </FormItem>
                <FormItem
                    {...formItemLayout}
                    label="所得成绩"
                >
                    {getFieldDecorator('grade', {
                        rules: [{required: true, message: '请选择所得成绩！'}],
                    })(
                        <RadioGroup>
                            <RadioButton value="A Range">A Range</RadioButton>
                            <RadioButton value="B Range">B Range</RadioButton>
                            <RadioButton value="C Range">C Range</RadioButton>
                            <RadioButton value="P/F">P/F</RadioButton>
                            <RadioButton value="Others">Others</RadioButton>
                        </RadioGroup>,
                    )}
                </FormItem>
                <FormItem {...formItemLayout} label="课程难度">
                    {getFieldDecorator('difficulty', {
                        rules: [{required: true, message: '请选择课程难度！'}],
                    })(
                        <Rate/>,
                    )}
                </FormItem>
                <FormItem {...formItemLayout} label="教授质量">
                    {getFieldDecorator('quality', {
                        rules: [{required: true, message: '请选择教授质量！'}],
                    })(
                        <Rate/>,
                    )}
                </FormItem>
                <FormItem {...formItemLayout} label="Workload">
                    {getFieldDecorator('workload', {
                        rules: [{required: true, message: '请选择Workload！'}],
                    })(
                        <Rate/>,
                    )}
                </FormItem>
                <FormItem {...formItemLayout} label="推荐指数">
                    {getFieldDecorator('recommend', {
                        rules: [{required: true, message: '请选择推荐指数！'}],
                    })(
                        <Rate/>,
                    )}
                </FormItem>
                <FormItem
                    {...formItemLayout}
                    label="相关建议"
                >
                    {getFieldDecorator('suggestion')(
                        <Textarea
                            rows={4}
                            style={{resize: 'none'}}
                            placeholder="就以上评分有任何具体原因或介绍，以及希望给想上这门课的同学的建议"
                        />,
                    )}
                </FormItem>
                <FormItem {...tailFormItemLayout}>
                    <Button type="primary" htmlType="submit">提交</Button>
                </FormItem>
            </Form>
        );
    }
}

RateMyProfessorForm = Form.create({})(RateMyProfessorForm);
export default RateMyProfessorForm;
