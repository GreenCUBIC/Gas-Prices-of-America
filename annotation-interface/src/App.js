import React from 'react';
import logo from './logo.svg';
import './App.css';
import {TwoDimensionalImage} from 'react-annotation-tool';

export default class extends React.Component {
  constructor(props) {
    super(props);
    this.urlParams = new URLSearchParams(window.location.search);
    this.imageUrl = this.urlParams.get('image_url');
    this.assignmentId = this.urlParams.get('assignmentId');
    this.hitId = this.urlParams.get('hitId');
    this.workerId = this.urlParams.get('workerId');
    this.turkSubmitTo = this.urlParams.get('turkSubmitTo');

    this.state = {
      imageUrl: this.imageUrl,
      answer: null,
    };
  }

  async submitAnnotation(annotation) {
    await this.setState({answer: annotation});
    this.form.submit();
  }

  render() {
    return (
      <div>
        <h1 style={{textAlign: 'center'}}>Gas price sign annotation</h1>
        <div
          style={{
            backgroundColor: '#f6f6f6',
            width: '75%',
            margin: '0 auto',
            border: '1px solid black',
          }}>
          <h2 style={{textAlign: 'center', backgroundColor: 'grey'}}>
            Instructions
          </h2>
          <div style={{display: 'flex', justifyContent: 'space-around'}}>
            <ol>
              <li>Click on add annotation</li>
              <li>
                Surround the gas price <i>sign</i> by clicking on the corners of
                the sign (not the individual prices)
              </li>
              <li>
                Bounding polygons should be tight and include the{' '}
                <b>entire portion of the sign that has the prices</b>
              </li>
              <li>
                If there is more than one sign, draw a bounding polygon for each
                sign
              </li>
              <li>If no sign is present, submit the HIT as is</li>
              <li>Click on submit</li>
            </ol>
            <img
              height={100}
              src="http://cu-bic.ca/public/segmentation-mturk-signlevel.png"
            />
          </div>
        </div>
        <div style={{width: '75%', margin: '0 auto'}}>
          <TwoDimensionalImage
            hasNextButton
            imageWidth={640}
            onNextClick={this.submitAnnotation.bind(this)}
            url={
              'https://www.brooks-signs.com/wp-content/uploads/2011/06/GulfPylon1.jpg?x29529'
            }
          />
        </div>
        <form
          ref={form => (this.form = form)}
          name="mturk_form"
          method="post"
          id="mturk_form"
          action={this.turkSubmitTo + '/mturk/externalSubmit'}>
          <input
            type="hidden"
            value={this.assignmentId}
            name="assignmentId"
            id="assignmentId"
          />
          <input
            type="hidden"
            value={'$$$' + JSON.stringify(this.state) + '$$$'}
            name="answer"
            id="answer"
          />
          <input
            style={{visibility: 'hidden'}}
            type="submit"
            id="mturk-submit"
            value="Submit"
          />
        </form>
      </div>
    );
  }
}
