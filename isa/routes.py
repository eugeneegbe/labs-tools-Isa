from flask import render_template, redirect, url_for, flash, request
from isa import app
from datetime import datetime
from isa import db
from isa.models import User, Campaign, Contribution
from isa.forms import CampaignForm, UpdateCampaignForm
import pycountry

@app.route( "/" )
def home():
    return render_template( 'home.html', title = 'Home' )

@app.route( "/campaigns" )
def getCampaigns():
    campaigns = Campaign.query.all()
    return render_template( 'campaigns.html', title = 'Campaigns',
        campaigns=campaigns, today_date=datetime.date( datetime.utcnow() ), datetime=datetime )

'''
    The below functions are used to perform operations on the db tables
'''

def sum_all_user_contributions(users):
    user_contribution_sum = 0;
    user_count = len(users)
    for user in users:
        user_contribution_sum += get_user_contributions( user.id )
    return user_contribution_sum

@app.route( "/campaigns/<string:campaign_name>" )
def getCampaignById( campaign_name ):
    # We select the campaign and the manager here
    campaign = Campaign.query.filter_by(campaign_name=campaign_name).first()
    campaign_manager = User.query.filter_by(id=campaign.user_id).first()

    # We get all the users from the db 
    all_users = User.query.all()
    all_contributions = Contribution.query.all()
    user_count = len(all_users)
    # contributions for campaign 
    campaign_contributions = 0
    #Editor for a particular campaign
    campaign_editors = 0
    # participantids for this campaign 
    campaign_users_ids = []

    # We are querrying all the users who participate in the campaign
    contribs_for_campaign = Contribution.query.filter_by( campaign_id=campaign.id ).all()
    for campaign_contribution in contribs_for_campaign:
        campaign_users_ids.append( campaign_contribution.user_id )  
    # we get the unique ids so as not to count an id twice
    campaign_users_ids_set = set( campaign_users_ids )

    campaign_editors = len( campaign_users_ids_set )
    # We then re-initialize the ids array
    campaign_users_ids = []
    
    # We now get the contributor count for this campaign
    for contrib in all_contributions:
        if (contrib.campaign_id == campaign.id ):
            campaign_contributions += 1
    return render_template( 'campaign.html', title = 'Campaign - ' + campaign_name,
                campaign=campaign, campaign_manager=campaign_manager.username,
                campaign_editors=campaign_editors, campaign_contributions=campaign_contributions,
            )

def get_country_from_code( country_code ):
    '''Retrieves the country from the country code

    :country_code string: The country code of the

    :returns:
    :rtype: String
    '''
    country = []
    countries = [ ( country.alpha_2, country.name ) for country in pycountry.countries ]
    for country_index in range( len( countries ) ):
        # index 0 is the country code selected from the form
        if( countries[ country_index ][ 0 ] == country_code ):
                country.append( countries[ country_index ] )
    return country[ 0 ][ 1 ]

def compute_campaign_status( end_date ):
    '''Determines the campaign status based on the end date

    :end_date Date: The campaign end date

    :returns:
    :rtype: Boolean
    '''
    status = bool( 'False' )
    if ( end_date.strftime("%Y-%m-%d %H:%M") < datetime.now().strftime("%Y-%m-%d %H:%M") ):
        status = bool( 'True' )
    return status
def testDbCommitSuccess():
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush() # for resetting non-commited .add()
        return True
    return False

@app.route( "/campaigns/create", methods=['GET','POST'] )
def CreateCampaign():
    form = CampaignForm()
    if form.is_submitted():
        # We add the campaign information to the database
        # TODO: Add current userid for user who created campaign
        campaign = Campaign(
            campaign_country = get_country_from_code( form.campaign_country.data ),
            campaign_name = form.campaign_name.data,
            categories = form.categories.data,
            start_date = form.start_date.data,
            end_date = form.end_date.data,
            status = compute_campaign_status( form.end_date.data ),
            description = form.description.data,
            user_id = 1
        )
        db.session.add( campaign )
        #commit failed
        if testDbCommitSuccess():
            flash( f'{ form.campaign_name.data } not created! Campaign may be available in { form.campaign_country.data }', 'danger' )
        else:
            flash( f'{ form.campaign_name.data } Campaign created!', 'success' )
            return redirect( url_for( 'getCampaigns' ) )
    return render_template( 'create_campaign.html', title = 'Create a campaign', form=form, datetime=datetime )

@app.route( "/campaigns/<string:campaign_name>/entry" )
def contributeToCampaign( campaign_name ):
    return render_template( 'campaign_entry.html', title = 'Contribute' )

@app.route( "/login" )
def login():
    return 'login'

@app.route( "/campaigns/<string:campaign_name>/update", methods=[ 'GET', 'POST' ] )
def updateCampaign( campaign_name ):
    form = UpdateCampaignForm()
    # when the form is submitted, we update the campaign
    # TODO: Check if campaign is closed so that it cannot be edited again
    # This is a potential issue/Managerial

    if form.is_submitted():
        campaign = Campaign.query.filter_by( campaign_name=campaign_name ).first()
        campaign.campaign_name = form.campaign_name.data
        campaign.description = form.description.data
        campaign.categories = form.categories.data
        campaign.campaign_country = get_country_from_code( form.campaign_country.data )
        campaign.start_date = form.start_date.data
        campaign.end_date = form.end_date.data

        if testDbCommitSuccess():
            flash( 'Please check the country for this Campaign!', 'danger' )

        else:
            flash( f'{ form.campaign_name.data } campaign Updated Succesfully!', 'success' )
            return redirect( url_for( 'getCampaigns' ) )
    # User requests to edit so we update the form with Campaign details
    elif request.method == 'GET':
        # we get the campaign data to place in form fields
        campaign = Campaign.query.filter_by( campaign_name = campaign_name ).first()
        form.campaign_name.data = campaign.campaign_name
        form.description.data = campaign.description
        form.categories.data = campaign.categories
        form.campaign_country.data = campaign.campaign_country
        form.start_date.data = campaign.start_date
        form.end_date.data = campaign.end_date
    else:
        flash( f'Booo! { form.campaign_name.data } Could not be updated!', 'danger' )
    return render_template( 'update_campaign.html', title = campaign_name + ' - Update', form=form )
