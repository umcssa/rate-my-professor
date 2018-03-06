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
    Select,
    Slider,
    DatePicker,
    Carousel,
    message,
} from 'antd';
import RateMyProfessorSearchResults from './RateMyProfessorSearchResults';

const $ = require('jquery');
const moment = require('moment');

const FormItem = Form.Item;
const RadioButton = Radio.Button;
const RadioGroup = Radio.Group;
const CheckboxGroup = Checkbox.Group;
const Textarea = Input.TextArea;
const Option = Select.Option;
const RangePicker = DatePicker.RangePicker;

const starNum = 5;

const apiRootPath = '/api/rate-my-professor/';


class RateMyProfessorSearch extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            confirmDirty: false,
            all_departments: [],
            all_courses: [],
            all_professors: [],
            semester: [moment('2015-01', 'YYYY-MM'), moment()],
            visible: false,
            results: {},
            totalPages: 0,
            currentPage: 1,
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.updateDepartment = this.updateDepartment.bind(this);
        this.handlePageChange = this.handlePageChange.bind(this);
    }

    componentDidMount() {
        $.ajax({
            method: 'GET',
            url: `${apiRootPath}get-viewable-departments/`,
        }).done((msg) => {
            this.setState({all_departments: JSON.parse(msg)});
        });
    }

    updateDepartment(department) {
        $.ajax({
            method: 'GET',
            url: `${apiRootPath}get-viewable-courses/?department=${department}`,
        }).done((msg) => {
            this.setState({all_courses: JSON.parse(msg)});
        });
        $.ajax({
            method: 'GET',
            url: `${apiRootPath}get-viewable-professors/?department=${department}`,
        }).done((msg) => {
            this.setState({all_professors: JSON.parse(msg)});
        });
    }

    handleSubmit(e) {
        e.preventDefault();
        this.setState({visible: true, results: {}, currentPage: 1});
        this.props.form.validateFieldsAndScroll((err, values) => {
            if (!err) {
                const data = values;
                data.difficulty = [data.difficulty[0] / starNum, data.difficulty[1] / starNum];
                data.quality = [data.quality[0] / starNum, data.quality[1] / starNum];
                data.workload = [data.workload[0] / starNum, data.workload[1] / starNum];
                data.recommend = [data.recommend[0] / starNum, data.recommend[1] / starNum];
                data.semester = [this.state.semester[0].format('YYYY-MM'), this.state.semester[1].format('YYYY-MM')];
                data.offset = 0;
                $.ajax({
                    method: 'POST',
                    url: `${apiRootPath}rmp-search/`,
                    data,
                }).done((msg) => {
                    const rawResults = JSON.parse(msg);
                    const results = {};
                    let i = rawResults.offset;
                    for (const rawResult of rawResults.results) {
                        i += 1;
                        results[i.toString()] = rawResult;
                    }
                    this.setState({results, totalPages: rawResults.total, currentPage: 1});
                    //console.log(this.state.results);
                });
            }
        });
    }

    handlePageChange(page) {
        this.setState({currentPage: page});
        if (!(page.toString() in this.state.results)) {
            this.props.form.validateFieldsAndScroll((err, values) => {
                if (!err) {
                    const data = values;
                    if (data !== {}) {
                        data.difficulty = [data.difficulty[0] / starNum, data.difficulty[1] / starNum];
                        data.quality = [data.quality[0] / starNum, data.quality[1] / starNum];
                        data.workload = [data.workload[0] / starNum, data.workload[1] / starNum];
                        data.recommend = [data.recommend[0] / starNum, data.recommend[1] / starNum];
                        data.semester = [this.state.semester[0].format('YYYY-MM'), this.state.semester[1].format('YYYY-MM')];
                        data.offset = page - 1;
                        $.ajax({
                            method: 'POST',
                            url: `${apiRootPath}rmp-search/`,
                            data,
                        }).done((msg) => {
                            const rawResults = JSON.parse(msg);
                            const results = Object.assign({}, this.state.results);
                            let i = rawResults.offset;
                            for (const rawResult of rawResults.results) {
                                i += 1;
                                results[i.toString()] = rawResult;
                            }
                            this.setState({results, totalPages: rawResults.total});
                        });
                    }
                }
            });
        }
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

        const grades = ['HU', 'SS', 'NS', 'ID', 'RE', 'Other'];
        const gradeOptions = [];
        for (let grade of grades) {
            gradeOptions.push(<Option key={grade}>{grade}</Option>);
        }

        return (
            <div>
                <RateMyProfessorSearchResults
                    results={this.state.results}
                    totalPages={this.state.totalPages}
                    page={this.state.currentPage}
                    visible={this.state.visible}
                    onCancel={() => {
                        this.setState({visible: false});
                    }}
                    onPageChange={this.handlePageChange}
                />
                <Form onSubmit={this.handleSubmit} style={{margin: 'auto', padding: 20, maxWidth: 1000}}>
                    <FormItem
                        {...formItemLayout}
                        label="课程院系"
                    >
                        {getFieldDecorator('department')(
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
                        {getFieldDecorator('course')(
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
                        {getFieldDecorator('professor')(
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
                        <RangePicker
                            placeholder={['Start month', 'End month']}
                            format="YYYY-MM"
                            value={this.state.semester}
                            mode={['month', 'month']}
                            onPanelChange={(value) => {
                                this.setState({
                                    semester: value,
                                });
                            }}
                        />
                    </FormItem>
                    <FormItem
                        {...formItemLayout}
                        label="学分数量"
                    >
                        {getFieldDecorator('credits', {initialValue: ['1', '2', '3', '4', '5']})(
                            <CheckboxGroup>
                                <Checkbox value="1">1</Checkbox>
                                <Checkbox value="2">2</Checkbox>
                                <Checkbox value="3">3</Checkbox>
                                <Checkbox value="4">4</Checkbox>
                                <Checkbox value="5">5</Checkbox>
                            </CheckboxGroup>,
                        )}
                    </FormItem>
                    <FormItem
                        {...formItemLayout}
                        label="课程类型"
                    >
                        {getFieldDecorator('type', {initialValue: ['HU', 'SS', 'NS', 'ID', 'RE', 'Other']})(
                            <Select
                                mode="multiple"
                                placeholder="Please select"
                                style={{width: '100%'}}
                            >
                                {gradeOptions}
                            </Select>,
                        )}
                    </FormItem>
                    <FormItem
                        {...formItemLayout}
                        label="所得成绩"
                    >
                        {getFieldDecorator('grade', {initialValue: ['A Range', 'B Range', 'C Range', 'P/F', 'Others']})(
                            <CheckboxGroup>
                                <Checkbox value="A Range">A Range</Checkbox>
                                <Checkbox value="B Range">B Range</Checkbox>
                                <Checkbox value="C Range">C Range</Checkbox>
                                <Checkbox value="P/F">P/F</Checkbox>
                                <Checkbox value="Others">Others</Checkbox>
                            </CheckboxGroup>,
                        )}
                    </FormItem>
                    <FormItem {...formItemLayout} label="课程难度">
                        {getFieldDecorator('difficulty', {initialValue: [0, starNum]})(
                            <Slider style={{maxWidth: 500}} range max={starNum}/>,
                        )}
                    </FormItem>
                    <FormItem {...formItemLayout} label="教授质量">
                        {getFieldDecorator('quality', {initialValue: [0, starNum]})(
                            <Slider style={{maxWidth: 500}} range max={starNum}/>,
                        )}
                    </FormItem>
                    <FormItem {...formItemLayout} label="Workload">
                        {getFieldDecorator('workload', {initialValue: [0, starNum]})(
                            <Slider style={{maxWidth: 500}} range max={starNum}/>,
                        )}
                    </FormItem>
                    <FormItem {...formItemLayout} label="推荐指数">
                        {getFieldDecorator('recommend', {initialValue: [0, starNum]})(
                            <Slider style={{maxWidth: 500}} range max={starNum}/>,
                        )}
                    </FormItem>
                    <FormItem {...tailFormItemLayout}>
                        <Button type="primary" htmlType="submit">搜索</Button>
                    </FormItem>
                </Form>
            </div>
        );
    }
}

RateMyProfessorSearch = Form.create({})(RateMyProfessorSearch);
export default RateMyProfessorSearch;
